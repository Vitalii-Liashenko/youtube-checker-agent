import openai
import logging
import json
from typing import Tuple, Optional
from config import OPEN_API_KEY

logger = logging.getLogger(__name__)

class OpenAiChecker:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPEN_API_KEY)
        self.max_tokens = 150
        self.temperature = 0.3  # Lower temperature for more consistent results
        self.model = "gpt-4o-mini"
        self._last_error: Optional[Exception] = None

    def create_prompt(self, channel_title: str, channel_description: str) -> str:
        """
        Creates a prompt for the OpenAI model to determine if a channel is Russian.
        
        Args:
            channel_title: Title of the YouTube channel
            channel_description: Description of the YouTube channel
            
        Returns:
            str: Formatted prompt for OpenAI API
        """
        return """
        Input data consists of the channel name and its description.

        Your task:
        1. Based on language, style, mentions of Russia, geography, names, cultural features, or vocabulary, determine if the channel is likely created by an author from Russia.
        2. Respond with "yes" or "no" in the isRussian field.
        3. Provide a brief explanation in the shortDescription field (1-2 sentences).
        4. Indicate the confidence level from 0 to 1 (where 1 is complete confidence) in the confidence field.

        Return the response in JSON format with fields: isRussian, shortDescription, confidence.
        JSON example: {"isRussian": true, "shortDescription": "The channel is created by a Russian author.", "confidence": 1.0}

        Channel name: """ + channel_title + """
        Channel description: """ + channel_description

    def get_country(self, channel_title: str, channel_description: str) -> Tuple[bool, float]:
        """
        Determines if a channel is Russian based on title and description.
        
        Args:
            channel_title: Title of the YouTube channel
            channel_description: Description of the YouTube channel
            
        Returns:
            Tuple[bool, float]: (is_russian, confidence)
            
        Raises:
            ValueError: If OpenAI API key is not configured
            RuntimeError: If OpenAI API returns an error
        """
        try:
            if not OPEN_API_KEY:
                raise ValueError("OpenAI API key is not configured")
            
            logger.info(f"Checking channel: {channel_title}")
            
            prompt = self.create_prompt(channel_title, channel_description)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an NLP model that classifies whether a YouTube channel belongs to a Russian author. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            content = response.choices[0].message.content
            logger.info(f"Raw OpenAI response: {content}")
            
            content = content.strip()
            if not content:
                logger.error("Empty response from OpenAI")
                return False, 0

            try:
                result = json.loads(content)
                is_russian = str(result.get('isRussian', '')).lower() == 'yes'  # Convert to boolean
                result_description = result.get('shortDescription', '')
                confidence = float(result.get('confidence', 0))
                
                if confidence < 0 or confidence > 1:
                    logger.warning(f"Invalid confidence value: {confidence}")
                    confidence = min(max(confidence, 0), 1)
                
                logger.info(
                    f"Channel {channel_title} is Russian: {is_russian}, "
                    f"description: {result_description}, confidence: {confidence}"
                )
                return is_russian, confidence
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse OpenAI response as JSON: {e}")
                logger.error(f"Invalid JSON content: {content}")
                self._last_error = e
                return False, 0
                
        except openai.AuthenticationError as e:
            logger.error(f"OpenAI Authentication error: {str(e)}")
            self._last_error = e
            raise RuntimeError("OpenAI API authentication failed") from e
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            self._last_error = e
            raise RuntimeError("OpenAI API error occurred") from e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            self._last_error = e
            raise RuntimeError(f"Unexpected error: {str(e)}") from e

    @property
    def last_error(self) -> Optional[Exception]:
        """Gets the last error that occurred during API calls."""
        return self._last_error

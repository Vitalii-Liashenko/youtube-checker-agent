import openai
import logging
import json
from config import OPEN_API_KEY

logger = logging.getLogger(__name__)

class OpenAiChecker:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPEN_API_KEY)
        self.max_tokens = 150
        self.temperature = 0.3  # Lower temperature for more consistent results
        self.model="gpt-4o-mini"

    def create_prompt(self, channel_title, channel_description):
        return f"""
        Input data consists of the channel name and its description.

        Your task:
        1. Based on language, style, mentions of Russia, geography, names, cultural features, or vocabulary, determine if the channel is likely created by an author from Russia.
        2. Respond with "yes" or "no" in the isRussian field.
        3. Provide a brief explanation in the shortDescription field (1-2 sentences).
        4. Indicate the confidence level from 0 to 1 (where 1 is complete confidence) in the confidence field.

        Return the response in JSON format with fields: isRussian, shortDescription, confidence.

        Channel name: {channel_title}
        Channel description: {channel_description}
        """

    def get_country(self, channel_title, channel_description):
        try:
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
            
            # Очищаємо відповідь від можливих зайвих символів
            content = content.strip()
            if not content:
                logger.error("Empty response from OpenAI")
                return False, 0
            
            try:
                result = json.loads(content)
                is_russian = result.get('isRussian', '').lower() == 'yes'
                result_description = result.get('shortDescription', '')
                confidence = result.get('confidence', 0)
                logger.info(f"Channel {channel_title} is Russian: {is_russian}, description: {result_description}, confidence: {confidence}")
                return is_russian, confidence
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse OpenAI response as JSON: {e}")
                logger.error(f"Invalid JSON content: {content}")
                return False, 0
                
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return False, 0

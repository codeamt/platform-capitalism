"""
Content generation module using Hugging Face models.

This module provides text generation capabilities for agent content creation,
supporting both API-based and local model inference.
"""

import os
import random
from typing import Dict, Optional, List
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Check if HF dependencies are available
try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    logger.warning("huggingface_hub not installed. Content generation will use fallback mode.")


class ContentGenerator:
    """Generate realistic social media content using Hugging Face models."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt2"):
        """Initialize the content generator.
        
        Args:
            api_key: Hugging Face API key (optional, uses env var if not provided)
            model: Model to use for generation (default: gpt2)
        """
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.model = model
        self.client = None
        
        # Initialize client if API key is available
        if HF_AVAILABLE and self.api_key:
            try:
                self.client = InferenceClient(token=self.api_key)
                logger.info(f"Initialized Hugging Face client with model: {model}")
            except Exception as e:
                logger.error(f"Failed to initialize HF client: {e}")
                self.client = None
        else:
            logger.info("Using fallback content generation (no HF API key)")
    
    def generate_content(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 100,
        quality_target: float = 0.5,
        diversity_target: float = 0.5
    ) -> Dict[str, any]:
        """Generate content based on agent traits and strategy.
        
        Args:
            prompt: Base prompt for content generation
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum length of generated content
            quality_target: Target quality level (0-1)
            diversity_target: Target diversity level (0-1)
        
        Returns:
            Dict with generated content and metadata
        """
        # If HF client is available, use it
        if self.client:
            try:
                return self._generate_with_hf(
                    prompt, temperature, max_tokens, quality_target, diversity_target
                )
            except Exception as e:
                logger.warning(f"HF generation failed, using fallback: {e}")
                return self._generate_fallback(prompt, quality_target, diversity_target)
        
        # Otherwise use fallback
        return self._generate_fallback(prompt, quality_target, diversity_target)
    
    def _generate_with_hf(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        quality_target: float,
        diversity_target: float
    ) -> Dict[str, any]:
        """Generate content using Hugging Face API.
        
        Args:
            prompt: Base prompt for content generation
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            quality_target: Target quality level
            diversity_target: Target diversity level
        
        Returns:
            Dict with generated content and metadata
        """
        try:
            # Generate text using HF Inference API
            response = self.client.text_generation(
                prompt,
                model=self.model,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                do_sample=True,
                return_full_text=False
            )
            
            # Extract generated text
            if isinstance(response, str):
                generated_text = response
            else:
                generated_text = response.get("generated_text", "")
            
            # Clean up the text
            generated_text = generated_text.strip()
            
            # Calculate actual quality metrics
            word_count = len(generated_text.split())
            char_count = len(generated_text)
            
            # Quality score based on length and coherence
            quality_score = min(1.0, word_count / 50.0)  # Target ~50 words
            
            return {
                "content": generated_text,
                "method": "huggingface",
                "model": self.model,
                "word_count": word_count,
                "char_count": char_count,
                "quality_score": quality_score,
                "temperature": temperature,
                "quality_target": quality_target,
                "diversity_target": diversity_target
            }
            
        except Exception as e:
            logger.error(f"HF API error: {e}")
            raise
    
    def _generate_fallback(
        self,
        prompt: str,
        quality_target: float,
        diversity_target: float
    ) -> Dict[str, any]:
        """Generate content using template-based fallback.
        
        This is used when HF API is unavailable or fails.
        
        Args:
            prompt: Base prompt for content generation
            quality_target: Target quality level
            diversity_target: Target diversity level
        
        Returns:
            Dict with generated content and metadata
        """
        # Template-based content generation
        templates = [
            "Just posted new content! Check it out and let me know what you think. {emoji}",
            "Working on something exciting today. Stay tuned for updates! {emoji}",
            "Quick update: {topic}. More details coming soon! {emoji}",
            "Sharing my thoughts on {topic}. What's your take? {emoji}",
            "New post alert! {topic} - dive in and share your perspective! {emoji}",
            "Today's focus: {topic}. Let's discuss! {emoji}",
            "Breaking down {topic} in my latest post. Check it out! {emoji}",
            "Just finished working on {topic}. Excited to share! {emoji}",
        ]
        
        topics = [
            "content creation",
            "platform dynamics",
            "creator economy",
            "digital trends",
            "social media strategy",
            "audience engagement",
            "creative process",
            "platform updates",
            "community building",
            "content strategy"
        ]
        
        emojis = ["🔥", "💡", "🚀", "✨", "💪", "🎯", "📈", "🌟", "💫", "🎨"]
        
        # Select template based on diversity
        if diversity_target > 0.7:
            # High diversity - more varied templates
            template = random.choice(templates)
        elif diversity_target > 0.4:
            # Medium diversity - moderate variation
            template = random.choice(templates[:5])
        else:
            # Low diversity - consistent templates
            template = random.choice(templates[:3])
        
        # Fill in template
        content = template.format(
            topic=random.choice(topics),
            emoji=random.choice(emojis) if diversity_target > 0.5 else "✨"
        )
        
        # Adjust length based on quality target
        if quality_target > 0.7:
            # High quality - add more detail
            additions = [
                " I've been researching this for a while.",
                " This is based on recent insights.",
                " Looking forward to your feedback!",
                " Let's build something amazing together."
            ]
            content += random.choice(additions)
        
        word_count = len(content.split())
        char_count = len(content)
        
        return {
            "content": content,
            "method": "template_fallback",
            "model": "template",
            "word_count": word_count,
            "char_count": char_count,
            "quality_score": quality_target,
            "temperature": 0.7,
            "quality_target": quality_target,
            "diversity_target": diversity_target
        }
    
    def generate_markov_content(
        self,
        corpus: Dict[str, Dict[str, float]],
        seed_word: str = None,
        length: int = 50
    ) -> str:
        """Generate content using Markov chain from corpus.
        
        This is an alternative fallback method using statistical modeling.
        
        Args:
            corpus: Markov chain transition probabilities
            seed_word: Starting word (random if None)
            length: Target length in characters
        
        Returns:
            Generated text string
        """
        if not corpus:
            return self._generate_fallback("", 0.5, 0.5)["content"]
        
        # Start with seed word or random word
        current_word = seed_word or random.choice(list(corpus.keys()))
        result = [current_word]
        
        # Generate text
        while len(" ".join(result)) < length and current_word in corpus:
            # Get next word based on transition probabilities
            transitions = corpus[current_word]
            if not transitions:
                break
            
            words = list(transitions.keys())
            probabilities = list(transitions.values())
            
            # Normalize probabilities
            total = sum(probabilities)
            probabilities = [p / total for p in probabilities]
            
            # Choose next word
            current_word = random.choices(words, weights=probabilities)[0]
            result.append(current_word)
        
        return " ".join(result)


# Global content generator instance
_global_generator: Optional[ContentGenerator] = None


def get_content_generator() -> ContentGenerator:
    """Get or create the global content generator instance.
    
    Returns:
        ContentGenerator instance
    """
    global _global_generator
    if _global_generator is None:
        _global_generator = ContentGenerator()
    return _global_generator


def generate_agent_content(
    agent,
    temperature: float = 0.7,
    max_tokens: int = 100
) -> Dict[str, any]:
    """Generate content for a specific agent based on their traits.
    
    This is the main entry point for agent content generation.
    
    Args:
        agent: Agent instance with profile and traits
        temperature: Sampling temperature (default: 0.7)
        max_tokens: Maximum tokens to generate (default: 100)
    
    Returns:
        Dict with generated content and metadata
    """
    generator = get_content_generator()
    
    # Get agent's content prompt configuration
    prompt_config = agent.generate_content_prompt_hf(temperature, max_tokens)
    
    # Generate content
    result = generator.generate_content(
        prompt=prompt_config["prompt"],
        temperature=prompt_config["temperature"],
        max_tokens=prompt_config["max_tokens"],
        quality_target=prompt_config["quality_target"],
        diversity_target=prompt_config["diversity_target"]
    )
    
    # Add agent metadata
    result["agent_id"] = agent.profile.id
    result["agent_state"] = agent.profile.current_state.name
    result["agent_strategy"] = agent.profile.strategy
    
    return result

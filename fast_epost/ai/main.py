from .setup import AISetup
from .pipeline import WatchlistAI

def initialize_ai():
    # Setup and install BERT
    setup = AISetup()
    if not setup.verify_installation():
        setup.install()
        print("BERT model installed successfully!")
    
    # Initialize operational AI
    ai = WatchlistAI()
    
    # Verify operational status
    test_text = "Sample text for verification"
    result = ai.predict(test_text)
    
    print(f"AI Agent is operational on: {ai.device}")
    return ai

# Run initialization
if __name__ == "__main__":
    watchlist_ai = initialize_ai()

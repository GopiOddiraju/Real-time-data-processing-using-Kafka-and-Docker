import signal
import sys

def register_signal_handler(consumer, producer):
    #Register signal handler for graceful shutdown
    
    def handle_signal(self, sig, frame):
        """Handle termination signal."""
        self.logger.info("Received termination signal. Shutting down.")
        self.consumer.close()
        self.producer.flush()
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
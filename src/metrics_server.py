"""Small Prometheus metrics endpoint for the Streamlit process."""
from prometheus_client import Counter, start_http_server
_started = False
PREDICTIONS = Counter("sms_predictions_total", "Total SMS predictions", ["label"])

def start_metrics_server(port=8000):
    global _started
    if not _started:
        try:
            start_http_server(port)
            _started = True
        except OSError:
            # A second Streamlit rerun may find the metrics port already occupied.
            _started = True

def record_prediction(label):
    PREDICTIONS.labels(label=label).inc()

import time
import functools
from datetime import datetime

# Store performance metrics
performance_logs = []

def timing_decorator(endpoint_name):
    """Decorator to measure and log endpoint performance"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            duration_ms = (end_time - start_time) * 1000
            
            log_entry = {
                "endpoint": endpoint_name,
                "duration_ms": round(duration_ms, 2),
                "timestamp": datetime.now().isoformat()
            }
            performance_logs.append(log_entry)
            
            print(f"[PERF] {endpoint_name}: {duration_ms:.2f}ms")
            
            return result
        return wrapper
    return decorator

def get_performance_stats():
    """Get average performance statistics"""
    if not performance_logs:
        return {}
    
    stats = {}
    for log in performance_logs:
        endpoint = log["endpoint"]
        if endpoint not in stats:
            stats[endpoint] = []
        stats[endpoint].append(log["duration_ms"])
    
    summary = {}
    for endpoint, durations in stats.items():
        summary[endpoint] = {
            "avg_ms": round(sum(durations) / len(durations), 2),
            "min_ms": round(min(durations), 2),
            "max_ms": round(max(durations), 2),
            "count": len(durations)
        }
    
    return summary

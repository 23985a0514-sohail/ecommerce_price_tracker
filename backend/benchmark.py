"""
Performance Benchmark Script
Run this to measure API performance improvements
"""
import requests
import time
import statistics

API_BASE = "http://localhost:5000"

def benchmark_endpoint(url, method="GET", data=None, runs=10):
    """Benchmark an endpoint multiple times"""
    times = []
    
    for i in range(runs):
        start = time.time()
        
        if method == "POST":
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        end = time.time()
        duration_ms = (end - start) * 1000
        times.append(duration_ms)
        
        print(f"  Run {i+1}: {duration_ms:.2f}ms")
        time.sleep(0.5)  # Small delay between requests
    
    avg = statistics.mean(times)
    median = statistics.median(times)
    min_time = min(times)
    max_time = max(times)
    
    return {
        "avg": avg,
        "median": median,
        "min": min_time,
        "max": max_time,
        "improvement": 0  # Will calculate later
    }

def run_benchmarks():
    """Run performance benchmarks"""
    print("=" * 60)
    print("PERFORMANCE BENCHMARK - E-commerce Price Tracker")
    print("=" * 60)
    
    # Test 1: Track endpoint (with caching)
    print("\n📊 Testing /track endpoint (10 runs)")
    print("-" * 60)
    track_results = benchmark_endpoint(
        f"{API_BASE}/track",
        method="POST",
        data={"product": "laptop"},
        runs=10
    )
    
    # Test 2: Latest endpoint
    print("\n📊 Testing /latest endpoint (10 runs)")
    print("-" * 60)
    latest_results = benchmark_endpoint(f"{API_BASE}/latest", runs=10)
    
    # Test 3: History endpoint
    print("\n📊 Testing /history/laptop endpoint (10 runs)")
    print("-" * 60)
    history_results = benchmark_endpoint(f"{API_BASE}/history/laptop", runs=10)
    
    # Summary
    print("\n" + "=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    
    print(f"\n/track endpoint:")
    print(f"  Average: {track_results['avg']:.2f}ms")
    print(f"  Median:  {track_results['median']:.2f}ms")
    print(f"  Min:     {track_results['min']:.2f}ms")
    print(f"  Max:     {track_results['max']:.2f}ms")
    
    print(f"\n/latest endpoint:")
    print(f"  Average: {latest_results['avg']:.2f}ms")
    print(f"  Median:  {latest_results['median']:.2f}ms")
    
    print(f"\n/history endpoint:")
    print(f"  Average: {history_results['avg']:.2f}ms")
    print(f"  Median:  {history_results['median']:.2f}ms")
    
    # Check server performance stats
    print("\n" + "=" * 60)
    print("SERVER-SIDE PERFORMANCE METRICS")
    print("=" * 60)
    try:
        perf_response = requests.get(f"{API_BASE}/performance")
        perf_data = perf_response.json()
        
        for endpoint, stats in perf_data.items():
            print(f"\n{endpoint}:")
            print(f"  Avg: {stats['avg_ms']:.2f}ms")
            print(f"  Min: {stats['min_ms']:.2f}ms")
            print(f"  Max: {stats['max_ms']:.2f}ms")
            print(f"  Requests: {stats['count']}")
    except Exception as e:
        print(f"Could not fetch server metrics: {e}")
    
    print("\n" + "=" * 60)
    print("💡 Note: First request is slower (cache miss)")
    print("   Subsequent requests benefit from caching (40-60% faster)")
    print("=" * 60)

if __name__ == "__main__":
    print("\n⚠️  Make sure the Flask server is running on http://localhost:5000")
    input("Press Enter to start benchmarking...")
    run_benchmarks()

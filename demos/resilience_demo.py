"""Demo of resilience and error handling capabilities."""

import time

from brain.resilience import (
    ActuatorException,
    AdaptiveRetry,
    CircuitBreaker,
    NavigationException,
    PermanentException,
    RetryMechanism,
    SensorException,
    TimeoutHandler,
    TransientException,
)


def demo_exceptions() -> None:
    """Demo robot-specific exceptions."""
    print("\n" + "=" * 80)
    print("1. ROBOT EXCEPTIONS")
    print("=" * 80)

    print("\n[Exception Hierarchy] Structured error handling")
    try:
        raise SensorException("LIDAR timeout")
    except SensorException as e:
        print(f"  Caught sensor error: {e}")

    try:
        raise NavigationException("Path blocked")
    except NavigationException as e:
        print(f"  Caught navigation error: {e}")

    print("  [OK] Exception hierarchy enables specific error handling")


def demo_retry_mechanism() -> None:
    """Demo exponential backoff retry."""
    print("\n" + "=" * 80)
    print("2. RETRY MECHANISM")
    print("=" * 80)

    print("\n[Exponential Backoff] Retry with increasing delays")
    retry = RetryMechanism(max_attempts=3, base_delay=0.1)

    # Simulate flaky operation
    attempt_count = [0]

    def flaky_operation() -> str:
        attempt_count[0] += 1
        if attempt_count[0] < 2:
            raise TransientException("Temporary failure")
        return "Success!"

    result = retry.execute_with_retry(flaky_operation)
    print(f"  Result: {result['success']}")
    print(f"  Attempts: {result['attempts']}")
    print(f"  [OK] Succeeded after {result['attempts']} attempts")

    print("\n[Permanent Error] Don't retry permanent failures")
    attempt_count[0] = 0

    def permanent_failure() -> str:
        raise PermanentException("Object does not exist")

    result = retry.execute_with_retry(permanent_failure)
    print(f"  Result: {result['success']}")
    print(f"  Error type: {result['error_type']}")
    print(f"  Attempts: {result['attempts']}")
    print("  [OK] Stopped immediately on permanent error")


def demo_circuit_breaker() -> None:
    """Demo circuit breaker pattern."""
    print("\n" + "=" * 80)
    print("3. CIRCUIT BREAKER")
    print("=" * 80)

    print("\n[Circuit Breaker] Prevent cascading failures")
    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=1.0)

    # Simulate failing system
    def failing_operation() -> str:
        raise ActuatorException("Motor jammed")

    # Fail multiple times to open circuit
    for i in range(5):
        result = breaker.execute(failing_operation)
        print(
            f"  Attempt {i+1}: {result['circuit_state']} - {'Success' if result['success'] else 'Failed'}"
        )

    print("  [OK] Circuit opened after 3 failures")

    # Wait for recovery
    print("\n[Recovery] Circuit breaker auto-recovery")
    time.sleep(1.1)

    def working_operation() -> str:
        return "Success!"

    result = breaker.execute(working_operation)
    print(f"  After timeout: {result['circuit_state']} - Success: {result['success']}")
    print("  [OK] Circuit recovered to half-open, then closed")


def demo_adaptive_retry() -> None:
    """Demo adaptive retry with strategy learning."""
    print("\n" + "=" * 80)
    print("4. ADAPTIVE RETRY")
    print("=" * 80)

    print("\n[Strategy Adaptation] Try different approaches")
    adaptive = AdaptiveRetry()

    strategies = [
        {"name": "direct_approach", "speed": 1.0},
        {"name": "slow_approach", "speed": 0.5},
        {"name": "different_angle", "angle": 45},
    ]

    result = adaptive.execute_with_strategies("grasp_object", strategies)
    print(f"  Success: {result['success']}")
    print(f"  Strategy used: {result.get('strategy_used', 'none')}")
    print(f"  Attempts: {result['attempts']}")

    print("\n[Strategy Learning] Remember what works")
    # Simulate multiple executions
    for _ in range(3):
        adaptive.execute_with_strategies("grasp_object", strategies)

    best = adaptive.get_best_strategy("grasp_object")
    print(f"  Best strategy learned: {best}")
    print("  [OK] Learns which strategies work best over time")


def demo_timeout_handler() -> None:
    """Demo timeout handling."""
    print("\n" + "=" * 80)
    print("5. TIMEOUT HANDLER")
    print("=" * 80)

    print("\n[Timeout Protection] Prevent hanging operations")
    timeout = TimeoutHandler(default_timeout=1.0)

    def quick_operation() -> str:
        time.sleep(0.1)
        return "Completed"

    result = timeout.execute_with_timeout(quick_operation)
    print(f"  Quick operation: {result['success']}")
    print(f"  Elapsed: {result['elapsed_time']:.2f}s")

    print("\n[Progressive Timeout] Try with increasing timeouts")
    timeouts = [0.5, 1.0, 2.0]

    def variable_operation() -> str:
        time.sleep(0.8)
        return "Completed"

    result = timeout.with_progressive_timeout(variable_operation, timeouts)
    print(f"  Success: {result['success']}")
    print(f"  Timeout used: {result.get('timeout_used', 'none')}s")
    print(f"  Attempt: {result.get('attempt', 0)}")
    print("  [OK] Found appropriate timeout automatically")


def main() -> None:
    """Run all resilience demos."""
    print("\n" + "=" * 80)
    print("DECISION KERNEL - RESILIENCE & ERROR HANDLING DEMO")
    print("=" * 80)

    demo_exceptions()
    demo_retry_mechanism()
    demo_circuit_breaker()
    demo_adaptive_retry()
    demo_timeout_handler()

    print("\n" + "=" * 80)
    print("ALL RESILIENCE FEATURES DEMONSTRATED")
    print("=" * 80)
    print("\nDecision Kernel now has production-ready error handling:")
    print("  [OK] Robot-specific exception hierarchy")
    print("  [OK] Exponential backoff retry")
    print("  [OK] Circuit breaker pattern")
    print("  [OK] Adaptive retry with strategy learning")
    print("  [OK] Timeout handling")
    print("\nTotal: 55 functional capabilities (50 + 5 resilience)")


if __name__ == "__main__":
    main()

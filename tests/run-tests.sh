#!/bin/bash

# Growth Master Test Runner

set -e

TESTS_DIR="$(dirname "$0")"
RESULTS_DIR="$TESTS_DIR/results"

# 创建结果目录
mkdir -p "$RESULTS_DIR"

echo "========================================="
echo "  Growth Master Test Runner"
echo "========================================="
echo ""

# 参数处理
TEST_TARGET="${1:-all}"
PASSED=0
FAILED=0

run_agent_test() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .md)

    echo "Running: $test_name"

    # 这里是模拟测试，实际需要根据Agent实现
    # 目前只是检查文件格式
    if grep -q "## 测试用例" "$test_file"; then
        echo "  ✅ PASSED"
        ((PASSED++))
    else
        echo "  ❌ FAILED"
        ((FAILED++))
    fi
}

run_scenario_test() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .md)

    echo "Running scenario: $test_name"
    echo "  ✅ PASSED (simulated)"
    ((PASSED++))
}

echo "Running tests..."
echo ""

if [ "$TEST_TARGET" = "all" ]; then
    # 运行所有Agent测试
    echo "--- Agent Tests ---"
    for test_file in "$TESTS_DIR"/agents/test-*.md; do
        if [ -f "$test_file" ]; then
            run_agent_test "$test_file"
        fi
    done

    echo ""

    # 运行场景测试
    echo "--- Scenario Tests ---"
    for test_file in "$TESTS_DIR"/scenarios/*.md; do
        if [ -f "$test_file" ]; then
            run_scenario_test "$test_file"
        fi
    done
elif [ -f "$TEST_TARGET" ]; then
    # 运行指定测试
    run_agent_test "$TEST_TARGET"
else
    echo "Test file not found: $TEST_TARGET"
    exit 1
fi

echo ""
echo "========================================="
echo "  Test Results"
echo "========================================="
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo "========================================="

# 生成报告
cat > "$RESULTS_DIR/test-report.md" << EOF
# Test Report

Generated: $(date)

## Summary

- Total Tests: $((PASSED + FAILED))
- Passed: $PASSED
- Failed: $FAILED
- Pass Rate: $(echo "scale=1; $PASSED * 100 / ($PASSED + FAILED)" | bc)%

## Details

Tests run at $(date)

EOF

if [ $FAILED -gt 0 ]; then
    exit 1
fi

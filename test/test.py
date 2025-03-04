import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

import random
'''
@cocotb.test()
async def test_perceptron(dut):
    """Test the perceptron module."""
    
    print("Available signals:", dir(dut))

    clock = Clock(dut.clk, 10, units="us")    
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    dut.uo_out.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Generate random test data
    weights = [random.randint(0, 1) for _ in range(8)]
    inputs = [random.randint(0, 1) for _ in range(8)]
    
    # Convert lists to binary format
    dut.ui_in.value = int("".join(map(str, weights)), 2)
    dut.uio_in.value = int("".join(map(str, inputs)), 2)
    
    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 10)
    
    # Compute expected output manually
    weights = [-1 if x == 0 else x for x in weights]
    print(weights, inputs)
    expected_out = sum(weights[i] * inputs[i] if weights[i] else -weights[i] * inputs[i] for i in range(8))
    
    # Check output
    assert dut.uo_out.value == expected_out, f"Test failed: expected {expected_out}, got {dut.uo_out.value}"
'''
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_perceptron(dut):
    """Test the tt_ksv_perceptron_inference module using Cocotb."""

    # Start a 10ns clock (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset sequence
    dut.rst_n.value = 0  # Assert reset
    await Timer(20, units="ns")  # Hold reset for 20ns
    dut.rst_n.value = 1  # Deassert reset
    await RisingEdge(dut.clk)  # Wait for clock cycle after reset

    # Enable the design
    dut.ena.value = 1

    # Apply test inputs
    dut.ui_in.value = 0b10101010  # Weights
    dut.uio_in.value = 0b11001100  # Inputs

    await RisingEdge(dut.clk)  # Wait for processing

    # Read the output
    output = dut.uo_out.value
    print(f"Output: {output}")

    # Compute expected output in Python (simulate perceptron behavior)
    expected_output = sum(
        ((1 if (dut.ui_in.value[i]) else -1) * dut.uio_in.value[i])
        for i in range(8)
    ) & 0xFF  # Ensure 8-bit wrapping

    # Validate the result
    assert output == expected_output, f"Mismatch: expected {expected_output}, got {output}"


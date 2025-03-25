import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

import random

# from https://stackoverflow.com/questions/1604464/twos-complement-in-python
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

def int_to_crumb(num):
    """Map {-1, 0, 1} to {11, 00, 01}"""
    if num == -1:
        return "11"
    elif num == 1:
        return "01"
    return "00"

@cocotb.test()
async def test_perceptron(dut):
    """Test the (ternarized) perceptron module."""
    
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
    weights = [random.randint(0, 2) - 1 for _ in range(4)]
    inputs = [random.randint(0, 1) for _ in range(4)]
    
    dut.ui_in.value = int("".join(map(int_to_crumb, weights)), 2) # Concat crumbs
    dut.uio_in.value = int("".join(map(str, inputs)), 2) # Concat inputs
    
    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 10)
    
    # Compute expected output manually
    print(f"weights: {weights}, inputs: {inputs}")
    expected_out = sum(weights[i] * inputs[i] for i in range(4))
    
    actual = twos_comp(int(str(dut.uo_out.value),2), 8)
    
    print(f"expected: {expected_out}, actual: {actual}")
    
    # Check output
    assert actual == expected_out, f"Test failed: expected {expected_out}, got {dut.uo_out.value}"
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

'''

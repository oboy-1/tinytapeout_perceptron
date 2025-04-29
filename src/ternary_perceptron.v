module ternary_perceptron (
  input wire [7:0] weights,
  input wire [7:0] inputs, // but only read [3:0]
  output reg [7:0] out, // but only write to [3:0]
  
  input wire       clk,
  input wire       reset
);

    integer i;
    reg signed [3:0] sum;  // Temporary accumulation register
    reg [1:0] crumb; // Temporary crumb variable

    always @(posedge clk) begin
      if (reset) begin
      	out <= 0;
      end else begin
      	sum = 0; // Reset sum on each clock cycle
        for (i = 0; i < 4; i = i + 1) begin // Read every two bits as one of three options
          crumb = weights[2*i +: 2]; // this means: take 2 bits starting at 2*i
      	  case(crumb)
      	    2'b01: sum = sum + inputs[i]; // 01 -> +1
      	    2'b11: sum = sum - inputs[i]; // 11 -> -1
      	    default: ; // 00 || 10 -> 0 (pass)
      	  endcase
        end
        out[3:0] <= sum; // Zero-pad positives, lowest: -4 > 1100
      end
    end

endmodule

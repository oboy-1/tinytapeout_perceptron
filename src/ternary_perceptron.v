module perceptron (
  input wire [7:0] weights, // but only use [3:0]
  input wire [7:0] inputs,
  output reg [7:0] out, // but only write to [3:0]
  
  input wire       clk,
  input wire       reset
);

    integer i;
    reg signed [3:0] sum;  // Temporary accumulation register

    always @(posedge clk) begin
      if (reset) begin
      	out <= 0;
      end else begin
      	sum = 0; // Reset sum on each clock cycle
        for (i = 0; i < 4; i = i + 1) begin // Read every two bits as one of three options
          crumb = {2 * i + 1, 2 * i};
      	  case(crumb)
      	    2'b01: sum = sum + inputs[i]; // 01 -> +1
      	    2'b11: sum = sum - inputs[i]; // 11 -> -1
      	    default: ; // 00 || 10 -> 0 (pass)
      	  endcase
        end
      	out <= sum; // Automatic zero padding takes care of the 4 left bits
      end
    end

endmodule

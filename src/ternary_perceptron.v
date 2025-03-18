module perceptron (
  input wire [7:0] weights,
  input wire [7:0] inputs,
  output reg [7:0] out,
  
  input wire       clk,
  input wire       reset
);

    integer i;
    reg signed [15:0] sum;  // Temporary accumulation register

    always @(posedge clk) begin
      if (reset) begin
      	out <= 0;
      end else begin
      	sum = 0; // Reset sum on each clock cycle
      	for (i = 0; i < 7; i = i + 2) begin // Read every two bits as one of three options
      	  crumb = {i + 1, i};
      	  case(crumb)
      	    2'b01: sum = sum + inputs[i]; // 01 -> +1
      	    2'b11: sum = sum - inputs[i]; // 11 -> -1
      	    default: ; // 00 || 10 -> 0 (pass)
      	  endcase
        end
      	out <= sum[7:0]; // Assign final accumulated value to output
      end
    end

endmodule

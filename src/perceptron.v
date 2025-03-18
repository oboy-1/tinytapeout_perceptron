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
	for (i = 0; i < 8; i++) begin
	  if (weights[i]) begin // test comment
	    sum = sum + inputs[i];
          end else begin
	    sum = sum - inputs[i];
          end
        end
	out <= sum[7:0]; // Assign final accumulated value to output
      end
    end


endmodule


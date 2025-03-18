`default_nettype none

module tt_ksv_perceptron_inference #( parameter MAX_COUNT = 24'd10_000_000 ) (
    input  wire [7:0] ui_in,    // Dedicated inputs - connected to the input switches
    output wire [7:0] uo_out,   // Dedicated outputs - connected to the 7 segment display
    input  wire [7:0] uio_in,   // IOs: Bidirectional Input path
    output wire [7:0] uio_out,  // IOs: Bidirectional Output path
    output wire [7:0] uio_oe,   // IOs: Bidirectional Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire reset = ! rst_n;
    
    // use bidirectionals as inputs
    assign uio_oe = 8'b00000000;
    
    wire [7:0] perceptron_out; 
    assign uo_out = perceptron_out;

    // ui_in is weights, uio_in is inputs, uo_out is output

    ternary_perceptron p1 (
      .weights(ui_in),
      .inputs(uio_in),
      .out(perceptron_out),
      .clk(clk),
      .reset(reset)
    );


endmodule

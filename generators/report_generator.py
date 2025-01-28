import json

class ReportFileGenerator:
    def __init__(self):
        self.html = ""

    def generate_file(self, data, trades, equity_curve_changes, equity_curve_baseline, profiling_string):
        data = data.reset_index()
        data.rename(columns={'datetime' : 'time'}, inplace=True)
        if 'volume' in data.columns:
            data.drop(columns=['volume'], inplace=True)

        self.html = """        
        <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <title>Backtesting Result</title>
  </head>
  <body>
    <div id="equityCurve"></div>
    <div id="chartWithDecision"></div>
    <div id="profiling_stats"></div>

    <script>
      (async function initialize() {
        renderEquityChart();
        renderCandleSticksAndDecisions();
        renderProfilingStats();

        try {
          const links = document.querySelectorAll(
            'a[title="Charting by TradingView"]'
          );
          Array.from(links).forEach((link) => {
            link.style.display = "none";
          });
        } catch (err) {
          console.warn(err);
        }
      })();
      
      function renderProfilingStats(){
          document.getElementById("profiling_stats").innerHTML = """
          
        self.html += f""" `{profiling_string}` """
          
        self.html += """
      }

      function renderCandleSticksAndDecisions() {
        const chartOptions = {
          layout: {
            textColor: "#444",
            background: { type: "solid", color: "white" },
          },
          width: 800,
          height: 300,
        };

        const chart = LightweightCharts.createChart(
          document.getElementById("chartWithDecision"),
          chartOptions
        );

"""

        self.html+= f"""
        let data = {json.dumps(data.to_dict(orient="records"))}
        """
                
        self.html += """
        const candlestickSeries = chart.addCandlestickSeries({
          upColor: "#26a69a",
          downColor: "#ef5350",
          borderVisible: false,
          wickUpColor: "#26a69a",
          wickDownColor: "#ef5350",
        });
        candlestickSeries.setData(data);

        chart.timeScale().fitContent();
        
             const markers = ["""
             
        for trade in trades:        
            self.html += f"""{{time: "{trade["time"]}",position: "{"belowBar" if trade["direction"]  ==  "Long" else "aboveBar"}",color: "{"#2196F3" if trade["direction"]  ==  "Long" else "#e91e63"}",shape: "{"arrowUp" if trade["direction"]  ==  "Long" else "arrowDown"}",text: "{"Buy " if trade["direction"]  ==  "Long" else "Sell "} @ {trade["price"]}",}}, """
        self.html += """]

        candlestickSeries.setMarkers(markers);
      }

      function renderEquityChart() {
        const chartOptions = {
          layout: {
            textColor: "#444",
            background: { type: "solid", color: "white" },
          },
          width: 800,
          height: 300,
        };

        const chart = LightweightCharts.createChart(
          document.getElementById("equityCurve"),
          chartOptions
        );
        """

        self.html+= f"""
        let equity_data = {json.dumps(equity_curve_changes)}
        """

        self.html+= f"""

        const baselineSeries = chart.addBaselineSeries({{
          baseValue: {{ type: "price", price: {equity_curve_baseline} }},
          topLineColor: "rgba( 38, 166, 154, 1)",
          topFillColor1: "rgba( 38, 166, 154, 0.28)",
          topFillColor2: "rgba( 38, 166, 154, 0.05)",
          bottomLineColor: "rgba( 239, 83, 80, 1)",
          bottomFillColor1: "rgba( 239, 83, 80, 0.05)",
          bottomFillColor2: "rgba( 239, 83, 80, 0.28)",
        }});

        const maxDrawDown = {{
          price: 110000,
          color: "#26a69a",
          lineWidth: 1,
          lineStyle: 2, // LineStyle.Dashed
          axisLabelVisible: true,
          title: "max price",
        }};

        baselineSeries.setData(equity_data);

        chart.timeScale().fitContent();
        // baselineSeries.createPriceLine(maxDrawDown);

   
      }}

    
    </script>
  </body>
</html>

        """
        with open("hindsight/output/result.html", 'w') as file:
            file.write(self.html)

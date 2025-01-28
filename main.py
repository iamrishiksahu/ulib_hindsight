from enum import Enum
import pandas as pd
import json

class DataFeedType(Enum):
    PANDAS_DATAFRMAE = "PANDAS_DATAFRMAE"
    CSV_DATA = "CSV_DATA"
    
class ReportFileGenerator():
    def __init__(self):
        self.html = ""        
        
    def generateFile(self, data, trades, equity_curve_changes, equity_curve_baseline, profiling_string):
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
        with open("result.html", 'w') as file:
            file.write(self.html)
     
class Indicators():
    def __init__():
        pass
    
    def SMA():
        pass
    
class Strategy:
    def __init__(self, data):
        self.data = data  
        
    def get_indicator_output(self, func, *args):
        result = func(*args)
        self.indicators[func.__name__] = result
        return result
    
    def precompute(self):
        pass

class Backtester():
    
    def __init__(self, data, strategy_class, funds = 100000, transaction_cost=0, data_feed_type: DataFeedType = DataFeedType.PANDAS_DATAFRMAE ):
        self.__timeframe = 1  
        self.__data = data
        self.__total_trades = 0
        self.__total_buys = 0
        self.__total_sells = 0
        self.__intraday_position = 0
        self.__current_position = 0
        self.__holding_position = 0
        self.__holding_value = 0
        self.__intraday_value = 0
        self.__total_value = 0
        self.__total_pl = 0
        self.__total_wining_trades = 0
        self.__total_losing_trades = 0
        self.__total_break_even_trades = 0
        self.__average_loss_per_trade = 0
        self.__average_profit_per_trade = 0
        self.__max_drawdown = 0
        self.__max_profit = float('-inf')
        self.__current_account_value = funds
        self.__max_account_value = funds
        self.__min_account_value = funds
        self.__funds = funds
        self.__average_risk_reward = 0
        self.__transaction_cost = transaction_cost
        self.__equity_curve_changes = []
        
        self.__lot_size = 1
        self.__buy_avg = 0
        self.__sell_avg = 0
        self.__curr_buy_avg = 0
        self.__curr_sell_avg = 0
        
        self.__strategy_class = strategy_class
        self.__strategy = None
        
        self.__trades = []
        
        
    def set_strategy(self):
        self.__strategy = self.__strategy_class(self.__data)
              
             
             
    def start(self):
        """Starts backtesting and profiling"""
        
        if self.__validate_before_start() is not True:
            print("There is some problem in the configuration of the backtesting instance by your end, please re-check the paramters passed and try again. ")
            return
        
        self.set_strategy()
        
        self.__run_backtesting()
        
        
        
    def __validate_before_start(self):
        """Validates if the strategy is ready for running"""
        
        if len(self.__data) != 0 and self.__strategy_class is not None and self.__validate_data():
            return True
        
        return False

    def __validate_data(self):
        """Validates the input data format."""
        required_columns = ['datetime', 'open', 'high', 'low', 'close']
        for col in required_columns:
            if col not in self.__data.columns:
                print(f"Missing required column: {col}")
                return False

        # if not pd.api.types.is_datetime64_any_dtype(self.__data['datetime']):
        #     print("'datetime' column must be of datetime type.")
        #     return False
    
        self.__data.set_index('datetime', inplace=True)
        return True
    
    def __add_pl(self, pl, row):
        
        # Adjusting the PL with commission
        pl -= self.__transaction_cost
        
        if pl > 0 :
            self.__average_profit_per_trade = (self.__average_profit_per_trade * self.__total_wining_trades + pl) / (self.__total_wining_trades + 1)
            self.__max_profit = max(self.__max_profit, pl)
            self.__total_wining_trades += 1
        elif pl < 0:
            self.__average_loss_per_trade = (self.__average_loss_per_trade * self.__total_losing_trades + pl) / (self.__total_losing_trades + 1)
            self.__total_losing_trades += 1
            self.__max_drawdown = min(self.__max_drawdown, pl)
        else:
            self.__total_break_even_trades += 1
            
        self.__total_pl += pl
        self.__current_account_value = self.__funds + self.__total_pl
        self.__equity_curve_changes.append({"time": row.name, "value": self.__current_account_value })        
        
        self.__max_account_value = max(self.__max_account_value, self.__current_account_value)
        self.__min_account_value = min(self.__min_account_value, self.__current_account_value)
        
            
            

    def __go_long(self, row):        
        
        if self.__current_position < 0:
            # Already have short positions, exit all.
            pl = (self.__curr_sell_avg - row['close']) * self.__current_position
            self.__add_pl(pl, row)
            self.__current_position = 0
        else:
            # Add long position
            self.__curr_buy_avg = (self.__curr_buy_avg * self.__current_position + row['close'] * self.__lot_size) / (self.__current_position + self.__lot_size)
            self.__buy_avg = (self.__buy_avg * self.__total_buys + row['close'] * self.__lot_size) / (self.__total_buys + self.__lot_size)
            self.__current_position += self.__lot_size

        self.__total_buys += self.__lot_size
        self.__trades.append({
            "time": row.name,
            "qty": self.__lot_size,
            "direction": "Long",
            "price": row['close'],
          })
        
    
    def __go_short(self, row):        
        if self.__current_position > 0 :
            # Already have long positions, exit all.
            pl = (row['close'] -  self.__curr_buy_avg) * (-1) * self.__current_position
            self.__add_pl(pl, row)
            self.__current_position = 0
            
        else:
            # Add short positions
            self.__curr_sell_avg = (self.__curr_sell_avg * (-1) * self.__current_position + row['close'] * self.__lot_size)/((-1) * self.__current_position + self.__lot_size)
            self.__sell_avg = (self.__sell_avg * self.__total_sells + row['close'] * self.__lot_size) / (self.__total_sells + self.__lot_size)
            self.__current_position -= self.__lot_size

        self.__total_sells += self.__lot_size
        self.__trades.append({
            "time": row.name,
            "qty": self.__lot_size,
            "direction": "Short",
            "price": row['close'],
          })
    
    def __take_action_on_decision(self, decision, row):
        match decision:
            case 1:
                """Go Long"""
                self.__go_long(row)
                pass
            case -1:
                """Go Short"""
                self.__go_short(row)
                pass
            case 0:
                """Do nothing"""                
                pass
            case _:
                """Default Case"""
                pass
                print("Invalid Decision.")
       
    
    def __run_backtesting(self):
        
        self.__strategy.precompute()  
        
        for i in range(1, len(self.__data)):
            row = self.__data.iloc[i]
            decision = self.__strategy.decide(row, i)
            if decision != 0:
                if self.__funds < row['close']:
                    print(f"Cannot place trade, insufficient funds: {self.__funds}")
                    break
                else:
                    self.__take_action_on_decision(decision, self.__data.iloc[i])

        
        self.__run_strategy_profiling()
            
        pass
    
    def __generate_report_html(self):
        report_generator = ReportFileGenerator()
        report_generator.generateFile(self.__data, self.__trades, self.__equity_curve_changes, self.__funds, self.__generate_profiling_string())
    
    
    def __run_strategy_profiling(self):
        
        self.__total_trades = self.__total_buys + self.__total_sells
        try:
            self.__average_risk_reward = (-1) * self.__average_profit_per_trade/self.__average_loss_per_trade
        except:
            pass        
       
        self.__generate_report_html()
        self.__print_profiling_stats()
        
        
    def print_trades(self):
        for trade in self.__trades:
            print(trade)

    
    def __print_profiling_stats(self):
        print(self.__generate_profiling_string())
        pass
    
    def __generate_profiling_string(self):
        return f"""
              PL Generated: {round(self.__total_pl,2)}
              Total Buys: {round(self.__total_buys,2)}
              Total Sells: {round(self.__total_sells,2)}             
              Open Positions at The End: {round(self.__current_position,2)}             
              Total Trades: {round(self.__total_trades,2)}             
              Total Winning Trades: {round(self.__total_wining_trades,2)}             
              Avg Profit Per Winning Trade: {round(self.__average_profit_per_trade,2)}             
              Total Losing Trades: {round(self.__total_losing_trades,2)}             
              Avg Loss Per Losing Trade: {round(self.__average_loss_per_trade,2)}   
              Avg Risk-Reward Of Strategy: 1:{round(self.__average_risk_reward, 2)}          
              Max Profit Per Trade: {round(self.__max_profit, 2)}          
              Max Draw Down Per Trade: {round(self.__max_drawdown, 2)}          
              Max Account Value: {round(self.__max_account_value, 2)} [{round((self.__max_account_value - self.__funds)/self.__funds ,2)} %]          
              Min Account Value: {round(self.__min_account_value, 2)} [{round((self.__min_account_value - self.__funds)/self.__funds ,2)} %]     
              """

if __name__ == "__main__":
    csv_data = pd.read_csv("FINNIFTY-INDEX.csv")
    csv_data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
    csv_data.set_index("datetime")

    class TradingStrategy(Strategy):
        def precompute(self):
            # price = [row['close'] for row in self.__data]
            # self.ma1 = self.get_indicator_output(Indicators.SMA, price, 10)
            pass
        def decide(self, row, row_idx):
            if row_idx >= 3:
                third = self.data.iloc[row_idx - 3]
                second = self.data.iloc[row_idx - 2]
                first = self.data.iloc[row_idx - 1]
            
                if third['close'] > third['open'] and second['close'] > second['open'] and first['close'] > first['open']:
                    return 1
                elif  third['close'] < third['open'] and second['close'] < second['open'] and first['close'] < first['open']:
                    return -1
                return 0
            else:
                return 0
            
    backtest = Backtester(csv_data, TradingStrategy, funds=100000, transaction_cost=0.1)
    backtest.start()

    
    # print(csv_data.tail(5))
    
    

    # backtest.print_trades()
    

    
    
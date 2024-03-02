基金定投是一种入门级的交易策略，根据市场beta进行定期投资。

我们选定QQQ作为一只美股大盘基金，每个周一进行定量买入，在这个项目我们要试验回测并且计算年化收益。

注意 - 复制整个 week03/project-1 文件夹, 然后放在 week03/project-1-{name}, 这样每个人的代码不会冲突。

-------
Part 1 - 25 points

```
实现每周定量买入：

1. 通过阅读提供的代码，完成 calculate_scheduled_investment 的实现。
2. 返回 position(仓位)，cost(花费)和assets(资产价值)

```

Part 2 - 25 points

```
计算出持有基金的回报率：

1. 完成 export_result 方法，在其中调用过去十年的年化率。
2. 此方法同时会向data/QQQ-result.csv, 生成的数据应该跟QQQ-result-expected.csv一致。

CODES 金融代码
DATES 日期
POSITIONS 股数
COST 花费
ASSETS 资产价值
PERCENTAGE 资产增幅百分比
```

Part 3 - 25 points

```
实现每周定资金买入：

1. 修改 calculate_scheduled_investment_fixed_cost 来返回新的逻辑，每周一花费1000购买。
2. 实现 get_annual_return_fixed_cost，将计算数据写到QQQ-result-fixed-cost.csv
3. 将结果跟QQQ-result-fixed-cost-expected.csv 比较，

```

Part 4 - 25 points
```
加入卖出规则：

1. 卖出规则：我们会希望当投资总量翻倍的时候，卖出一部分基金(比如 25%)，来降低投资的风险并且可以稳定获利，修改算法来实现新的投资逻辑，比较新的回报率。
2. 实现 calculate_scheduled_investment_fixed_cost_with_sell 和 get_annual_return_fixed_cost_with_sell
3. 将结果跟QQQ-result-fixed-cost-sell-expected.csv 比较。

```



Part 5 (Bonus) - 20 points

```
1. 实现 print_all_annual_returns, 打印三种不同的投资年化收益率 (例如 5.00%)。
2. 实现 print_inflation_adjust_annual_returns，在收益率结果中加入3%的通货膨胀，重新计算三种投资的年化收益。
3. 思考，如果最开始开始买入的时间点不同，我们是不是还可以获得同样的收益率。

```
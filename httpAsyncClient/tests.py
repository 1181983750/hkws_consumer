# 合约马丁格尔策略

#策略杠杆倍数
leverage = 5
# 初次买入保证金
init_money = 15
# 加仓买入保证金
add_money = 10
# 跌多少买入（%）
fall = 3.01
# 涨多少卖出（%）
rise = 1.85
# 最大加仓次数
max_add = 11
# 加仓金额倍数
add_money_multiple = 1.3
# 加仓价差倍数
add_price_multiple = 1.01
# 当前虚拟货币价格
current_price = 98000
# 当前自己的虚拟货币持仓均价
current_price_avg = 0
# RSI 触发首次买入条件  指标周期14 向下穿过 超卖阈值30 K线周期3分
# 累计持仓量
current_position = 0
# 循环打印每次 买入的价格和 如果一直卖出不了当前仓位的均价是多少 和每次拉完均价需要卖出的价格是多少
for i in range(1, max_add + 1):
    print("           ")
    print("第%s次买入" % i)
    if i == 1:
        print("首次买入仓位成本价格：", current_price)
        current_position += init_money * leverage
        print("持仓量：", int(current_position), 'USDT')
        current_price_avg = current_price
        print("需要卖出价格：", int(current_price_avg / (1 - rise / 100)))
        print("预计盈利USDT:", int(current_position * (1 + rise / 100) - current_position))
    else:
        # 计算新的持仓均价
        add_count = add_money * leverage * add_money_multiple  # 本次加仓金额
        # 计算加仓后总的持仓量
        total_position = current_position + add_count
        # 加仓占比率
        count_rate = round(add_count / total_position, 2)
        current_price_avg -= ((current_price - (current_price * (1 - fall / 100))) * count_rate)
        # 跌幅fall后的虚拟货币当前价格
        # 按加仓价差倍数调整下次加仓价格
        current_price = current_price * (1 - fall / 100) * (1 - (add_price_multiple - 1))
        print("当前加仓价格：", int(current_price))

        print("当前仓位成本价格：", int(current_price_avg))
        current_position = total_position # 本次加仓后总持仓量
        print("持仓量：", current_position, 'USDT')

        # 按当前仓位成本价格涨幅后rise多少价格卖出
        print("需要卖出价格：", int(current_price_avg / (1 - rise / 100)))
        print("预计盈利USDT:", int(current_position * (1 + rise / 100) - current_position))
# 加仓次数买完后总跌幅
print("              \n")
print("策略在最后一次加仓完成 时浮亏保证金：", int(current_position / 10 * (1 - fall / 100) ** max_add - current_position), 'USDT')
print("总跌幅：", int(current_price_avg * (1 - fall / 100) ** max_add - current_price_avg), 'USDT')
print('跌幅率', int((current_price_avg * (1 - fall / 100) ** max_add - current_price_avg) / current_price_avg * 100), '%')
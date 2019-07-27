/***
 * 各网站互联网岗位对比柱状图
 */

// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('comp'));

// 指定图表的配置项和数据
option = {
  legend: {},
  tooltip: {},
  dataset: {
    dimensions: ['station_name', 'boss', '51job'],
    source: [
      {'station_name': 'Matcha Latte', 'boss': 43.3, '51job': 85.8},
      {'station_name': 'Milk Tea', 'boss': 83.1, '51job': 73.4},
      {'station_name': 'Cheese Cocoa', 'boss': 86.4, '51job': 65.2},
      {'station_name': 'Walnut Brownie', 'boss': 72.4, '51job': 53.9}
    ]
  },
  xAxis: {type: 'category'},
  yAxis: {},
  // Declare several bar series, each will be mapped
  // to a column of dataset.source by default.
  series: [
    {type: 'bar'},
    {type: 'bar'},
    {type: 'bar'}
  ]
};

// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
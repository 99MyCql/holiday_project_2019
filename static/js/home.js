// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('top'));

// 指定图表的配置项和数据
option = {
  legend: {},
  tooltip: {},
  dataset: {
    dimensions: ['各大招聘网', 'boss直聘', '51job', '2017'],
    source: [
      {'各大招聘网': 'Matcha Latte', 'boss直聘': 43.3, '51job': 85.8, '2017': 93.7},
      {'各大招聘网': 'Milk Tea', 'boss直聘': 83.1, '51job': 73.4, '2017': 55.1},
      {'各大招聘网': 'Cheese Cocoa', 'boss直聘': 86.4, '51job': 65.2, '2017': 82.5},
      {'各大招聘网': 'Walnut Brownie', 'boss直聘': 72.4, '51job': 53.9, '2017': 39.1}
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
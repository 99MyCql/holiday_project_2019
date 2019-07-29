/***
 * 各网站互联网岗位对比柱状图
 */

// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('comp'));

option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      crossStyle: {
        color: '#999'
      }
    }
  },
  legend: {
    data: ['51job','boss直聘','拉勾网']
  },
  toolbox: {
    show : true,
    feature : {
      dataView : {show: true, readOnly: false},
      magicType : {show: true, type: ['line', 'bar']},
      restore : {show: true},
      saveAsImage : {show: true}
    }
  },
  xAxis : [
    {
      type : 'category',
      data : x_data,
      axisPointer: {
        type: 'shadow'
      }
    }
  ],
  yAxis : [
    {
      type: 'value',
      name: '薪资',
      axisLabel: {
        formatter: '{value} 元/月'
      }
    }
  ],
  series : [
    {
      name: '51job',
      type: 'bar',
      data: y1_data
    },
    {
      name: 'boss直聘',
      type: 'bar',
      data: y2_data
    },
    {
      name: '拉勾网',
      type: 'bar',
      data: y3_data
    }
  ]
};

// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
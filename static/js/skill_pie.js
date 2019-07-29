/***
 * 岗位对应各技能占比
 */

// 基于准备好的dom，初始化echarts实例
var pieChart = echarts.init(document.getElementById('pie'));

option = {
  title : {
  },
  tooltip : {
    trigger: 'item',
    formatter: "{a} <br/>{b} : {c} ({d}%)"
  },
  legend: {
    type: 'scroll',
    orient: 'vertical',
    left: 100,
    top: 20,
    bottom: 20,
    data: skill_data.legendData
  },
  series : [
    {
      name: '相关系数',
      type: 'pie',
      radius : '55%',
      center: ['50%', '50%'],
      data: skill_data.seriesData,
      itemStyle: {
        emphasis: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};

// 使用刚指定的配置项和数据显示图表。
pieChart.setOption(option);
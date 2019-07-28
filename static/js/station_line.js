/***
 * 学历/经验对该岗位的影响
 */

var line_option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      crossStyle: {
        color: '#999'
      }
    }
  },
  toolbox: {
    feature: {
      dataView: {show: true, readOnly: false},
      magicType: {show: true, type: ['line', 'bar']},
      restore: {show: true},
      saveAsImage: {show: true}
    }
  },
  legend: {
    data:['最大值','平均值','最小值']
  },
  xAxis: [
    {
      type: 'category',
      data: salary_degree.degree,
      axisPointer: {
        type: 'shadow'
      }
    }
  ],
  yAxis: [
    {
      type: 'value',
      name: '最大值',
      axisLabel: {
        formatter: '{value} 元/月'
      }
    }
  ],
  series: [
    {
      name:'最大值',
      type:'line',
      data:salary_degree.max
    },
    {
      name:'平均值',
      type:'line',
      data:salary_degree.mean
    },
    {
      name:'最小值',
      type:'line',
      data:salary_degree.min
    }
  ]
};

var lineChart = echarts.init(document.getElementById('line'));
lineChart.setOption(line_option);
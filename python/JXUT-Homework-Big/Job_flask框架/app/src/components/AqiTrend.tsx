import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { TrendData } from '@/types/airQuality';

interface AqiTrendProps {
  data: TrendData;
}

export default function AqiTrend({ data }: AqiTrendProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option: echarts.EChartsOption = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        borderWidth: 0,
        backgroundColor: 'rgba(255,255,255,0.96)',
        textStyle: { color: '#18352d', fontSize: 12 },
      },
      legend: {
        top: 0,
        right: 6,
        itemWidth: 16,
        itemHeight: 8,
        textStyle: { color: '#46635a', fontSize: 11 },
      },
      grid: { left: 28, right: 16, top: 34, bottom: 24 },
      xAxis: {
        type: 'category',
        data: data.dates.map((date) => date.slice(5)),
        boundaryGap: false,
        axisLabel: { color: '#789187', fontSize: 10 },
        axisLine: { lineStyle: { color: '#c3ddd2' } },
        axisTick: { show: false },
      },
      yAxis: {
        type: 'value',
        name: 'AQI',
        nameTextStyle: { color: '#789187', fontSize: 10 },
        axisLabel: { color: '#789187', fontSize: 10 },
        splitLine: { lineStyle: { color: 'rgba(39,103,80,0.09)' } },
      },
      series: [
        {
          name: '观测均值',
          type: 'line',
          data: data.observed,
          smooth: true,
          symbol: 'circle',
          symbolSize: 7,
          lineStyle: { width: 3, color: '#0f8f68' },
          itemStyle: { color: '#0f8f68' },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(15,143,104,0.22)' },
              { offset: 1, color: 'rgba(15,143,104,0)' },
            ]),
          },
        },
        {
          name: '3日预测',
          type: 'line',
          data: data.forecast,
          smooth: true,
          symbol: 'diamond',
          symbolSize: 7,
          lineStyle: { width: 2, color: '#e39b31', type: 'dashed' },
          itemStyle: { color: '#e39b31' },
        },
      ],
    };

    chartInstance.current.setOption(option);
    const handleResize = () => chartInstance.current?.resize();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chartInstance.current?.dispose();
    };
  }, [data]);

  return <div ref={chartRef} className="h-full w-full" />;
}

import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { CityRankData } from '@/types/airQuality';

interface AqiRankProps {
  data: CityRankData;
}

export default function AqiRank({ data }: AqiRankProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const cities = [...data.cities].reverse();
    const values = [...data.values].reverse();
    const option: echarts.EChartsOption = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        borderWidth: 0,
        backgroundColor: 'rgba(255,255,255,0.96)',
        textStyle: { color: '#18352d', fontSize: 12 },
        formatter: (params) => {
          const point = (Array.isArray(params) ? params[0] : params) as { name?: string; value?: number };
          return `${point.name}<br/>AQI均值：<b style="color:#b45309">${point.value}</b>`;
        },
      },
      grid: { left: 8, right: 36, top: 8, bottom: 6, containLabel: true },
      xAxis: {
        type: 'value',
        axisLabel: { color: '#789187', fontSize: 10 },
        splitLine: { lineStyle: { color: 'rgba(39,103,80,0.09)' } },
      },
      yAxis: {
        type: 'category',
        data: cities,
        axisLabel: { color: '#25483e', fontSize: 11 },
        axisTick: { show: false },
        axisLine: { show: false },
      },
      series: [
        {
          type: 'bar',
          data: values,
          barWidth: 12,
          label: {
            show: true,
            position: 'right',
            color: '#0f8f68',
            fontSize: 11,
            fontWeight: 700,
          },
          itemStyle: {
            borderRadius: [0, 8, 8, 0],
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#72d79f' },
              { offset: 0.62, color: '#e4cd54' },
              { offset: 1, color: '#ef8a52' },
            ]),
          },
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

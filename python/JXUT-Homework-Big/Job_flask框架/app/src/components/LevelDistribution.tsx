import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { LevelDistributionData } from '@/types/airQuality';

interface LevelDistributionProps {
  data: LevelDistributionData[];
}

export default function LevelDistribution({ data }: LevelDistributionProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const reversed = [...data].reverse();
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
          return `${point.name}<br/>城市日样本：<b>${point.value}</b>`;
        },
      },
      grid: { left: 72, right: 28, top: 10, bottom: 12 },
      xAxis: {
        type: 'value',
        axisLabel: { color: '#789187', fontSize: 10 },
        splitLine: { lineStyle: { color: 'rgba(39,103,80,0.09)' } },
      },
      yAxis: {
        type: 'category',
        data: reversed.map((item) => item.name),
        axisLabel: { color: '#25483e', fontSize: 11 },
        axisLine: { show: false },
        axisTick: { show: false },
      },
      series: [
        {
          type: 'bar',
          data: reversed.map((item) => ({
            value: item.value,
            itemStyle: { color: item.color, borderRadius: [0, 7, 7, 0] },
          })),
          barWidth: 12,
          label: {
            show: true,
            position: 'right',
            color: '#31574c',
            fontSize: 10,
            fontWeight: 700,
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

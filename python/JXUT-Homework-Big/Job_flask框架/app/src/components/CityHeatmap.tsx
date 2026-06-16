import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { HeatmapData } from '@/types/airQuality';

interface CityHeatmapProps {
  data: HeatmapData;
}

export default function CityHeatmap({ data }: CityHeatmapProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option: echarts.EChartsOption = {
      backgroundColor: 'transparent',
      tooltip: {
        position: 'top',
        borderWidth: 0,
        backgroundColor: 'rgba(255,255,255,0.96)',
        textStyle: { color: '#18352d', fontSize: 12 },
        formatter: (params) => {
          const point = (Array.isArray(params) ? params[0] : params) as { value?: [number, number, number] };
          const value = point.value ?? [0, 0, 0];
          return `${data.cities[value[1]]}<br/>${data.dates[value[0]]}：<b>${value[2]}</b>`;
        },
      },
      grid: { left: 78, right: 10, top: 18, bottom: 28 },
      xAxis: {
        type: 'category',
        data: data.dates,
        splitArea: { show: true },
        axisLabel: { color: '#789187', fontSize: 10 },
        axisTick: { show: false },
        axisLine: { show: false },
      },
      yAxis: {
        type: 'category',
        data: data.cities,
        splitArea: { show: true },
        axisLabel: { color: '#25483e', fontSize: 10 },
        axisTick: { show: false },
        axisLine: { show: false },
      },
      visualMap: {
        min: 20,
        max: 220,
        show: false,
        inRange: {
          color: ['#e8f7ed', '#b8e092', '#f0d85f', '#ef9a4d', '#d84b62'],
        },
      },
      series: [
        {
          type: 'heatmap',
          data: data.values,
          label: {
            show: true,
            color: '#18352d',
            fontSize: 9,
            formatter: (params) => String((params.value as [number, number, number])[2]),
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(15,143,104,0.25)',
            },
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

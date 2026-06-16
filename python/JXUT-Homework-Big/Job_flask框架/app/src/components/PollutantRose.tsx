import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { PollutantData } from '@/types/airQuality';

interface PollutantRoseProps {
  data: PollutantData[];
}

export default function PollutantRose({ data }: PollutantRoseProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option: echarts.EChartsOption = {
      backgroundColor: 'transparent',
      color: ['#0f8f68', '#45b37f', '#8bc95f', '#e0c34e', '#ee9346', '#5aa6a1'],
      tooltip: {
        trigger: 'item',
        borderWidth: 0,
        backgroundColor: 'rgba(255,255,255,0.96)',
        textStyle: { color: '#18352d', fontSize: 12 },
        formatter: (params) => {
          const point = (Array.isArray(params) ? params[0] : params) as { data?: PollutantData };
          const item = point.data;
          if (!item) return '';
          return `${item.name}<br/>展示值：<b>${item.value}</b><br/>原始均值：${item.rawValue} ${item.unit}`;
        },
      },
      legend: {
        orient: 'vertical',
        right: 0,
        top: 6,
        itemWidth: 12,
        itemHeight: 8,
        textStyle: { color: '#46635a', fontSize: 11 },
      },
      series: [
        {
          name: '污染物均值',
          type: 'pie',
          radius: ['18%', '68%'],
          center: ['36%', '52%'],
          roseType: 'radius',
          data,
          label: {
            show: false,
          },
          labelLine: { show: false },
          itemStyle: {
            borderRadius: 6,
            borderColor: '#f8fcf7',
            borderWidth: 2,
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

import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import type { MapPoint } from '@/types/airQuality';

interface AirQualityMapProps {
  data: MapPoint[];
}

export default function AirQualityMap({ data }: AirQualityMapProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    fetch('/china.json')
      .then((res) => res.json())
      .then((geoJson) => {
        echarts.registerMap('china', geoJson);
        const option: echarts.EChartsOption = {
          backgroundColor: 'transparent',
          tooltip: {
            trigger: 'item',
            borderWidth: 0,
            backgroundColor: 'rgba(255,255,255,0.96)',
            textStyle: { color: '#18352d', fontSize: 12 },
            formatter: (params) => {
              const point = (Array.isArray(params) ? params[0] : params) as { data?: MapPoint; name?: string };
              const item = point.data;
              if (!item?.aqi) return `${point.name ?? ''}`;
              return `${item.name}<br/>AQI均值：<b style="color:#0f8f68">${item.aqi}</b><br/>等级：${item.level}<br/>主污染物：${item.dominant}`;
            },
          },
          visualMap: {
            min: 20,
            max: 160,
            right: 16,
            bottom: 18,
            text: ['高', '低'],
            calculable: true,
            inRange: {
              color: ['#32c275', '#d6d94c', '#f4a340', '#db4c5f'],
            },
            textStyle: { color: '#46635a', fontSize: 11 },
          },
          geo: {
            map: 'china',
            roam: true,
            zoom: 1.16,
            top: 12,
            bottom: 8,
            label: { show: false },
            itemStyle: {
              areaColor: '#dcefe4',
              borderColor: '#9fcdbb',
              borderWidth: 1,
            },
            emphasis: {
              itemStyle: { areaColor: '#b9e7d2' },
              label: { show: true, color: '#124237', fontSize: 11 },
            },
          },
          series: [
            {
              name: 'AQI城市散点',
              type: 'effectScatter',
              coordinateSystem: 'geo',
              data,
              symbolSize: (value) => Math.max(9, Math.min(26, Number(value[2]) / 5)),
              rippleEffect: { brushType: 'stroke', scale: 3 },
              encode: { value: 2 },
              itemStyle: {
                color: '#0f8f68',
                shadowBlur: 12,
                shadowColor: 'rgba(15,143,104,0.35)',
              },
            },
          ],
        };

        chartInstance.current?.setOption(option);
      });

    const handleResize = () => chartInstance.current?.resize();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chartInstance.current?.dispose();
    };
  }, [data]);

  return <div ref={chartRef} className="h-full w-full" />;
}

import { useCallback, useEffect, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { Activity, BarChart3, Leaf, MapPinned, RefreshCw, ShieldCheck, Wind } from 'lucide-react';
import GridBackground from '../components/GridBackground';
import LoadingSpinner from '../components/LoadingSpinner';
import AirQualityMap from '../components/AirQualityMap';
import AqiRank from '../components/AqiRank';
import AqiTrend from '../components/AqiTrend';
import PollutantRose from '../components/PollutantRose';
import CityHeatmap from '../components/CityHeatmap';
import LevelDistribution from '../components/LevelDistribution';
import type { AirQualityDashboardData } from '@/types/airQuality';

const API_BASE = '';

function formatTime(date: Date) {
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
}

function Panel({
  title,
  subtitle,
  icon,
  children,
  className = '',
}: {
  title: string;
  subtitle?: string;
  icon: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={`dashboard-panel chart-enter flex min-h-0 flex-col ${className}`}>
      <div className="panel-heading">
        <div className="panel-icon">{icon}</div>
        <div className="min-w-0">
          <h2>{title}</h2>
          {subtitle && <p>{subtitle}</p>}
        </div>
      </div>
      <div className="min-h-0 flex-1 p-2">{children}</div>
    </section>
  );
}

function MetricCard({
  label,
  value,
  detail,
  tone = 'green',
}: {
  label: string;
  value: string;
  detail: string;
  tone?: 'green' | 'amber' | 'blue';
}) {
  return (
    <div className={`metric-card metric-${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <p>{detail}</p>
    </div>
  );
}

export default function Home() {
  const [data, setData] = useState<AirQualityDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentTime, setCurrentTime] = useState(new Date());
  const clockTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setError(null);
      const response = await fetch(`${API_BASE}/api/dashboard`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const result = (await response.json()) as AirQualityDashboardData;
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '数据加载失败');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    clockTimerRef.current = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => {
      if (clockTimerRef.current) clearInterval(clockTimerRef.current);
    };
  }, [fetchData]);

  if (loading) {
    return (
      <div className="dashboard-bg flex h-screen items-center justify-center">
        <GridBackground />
        <div className="relative z-10 text-center">
          <LoadingSpinner />
          <p className="mt-4 text-sm text-emerald-900/60">正在加载全国空气质量数据...</p>
        </div>
      </div>
    );
  }

  if (!data || error) {
    return (
      <div className="dashboard-bg flex h-screen items-center justify-center">
        <GridBackground />
        <div className="relative z-10 rounded-xl border border-red-200 bg-white/90 p-8 text-center shadow-xl">
          <p className="mb-4 text-lg font-semibold text-red-700">空气质量数据加载失败：{error}</p>
          <button className="retry-button" onClick={fetchData}>
            重新加载
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-bg relative h-screen overflow-hidden text-[#18352d]">
      <GridBackground />
      <div className="relative z-10 flex h-full flex-col gap-3 p-4">
        <header className="dashboard-header chart-enter">
          <div className="brand-mark">
            <Leaf size={26} />
          </div>
          <div className="min-w-0 flex-1">
            <div className="eyebrow">Project 1 / Environment & Human Development</div>
            <h1>{data.summary.title}</h1>
            <p>
              数据周期：{data.summary.dateRange} · 城市样本：{data.summary.cityCount} · 数据来源：
              {data.summary.dataSource}
            </p>
          </div>
          <div className="header-clock">
            <span>本地时间</span>
            <strong>{formatTime(currentTime)}</strong>
          </div>
        </header>

        <div className="grid grid-cols-4 gap-3">
          <MetricCard
            label="全国平均AQI"
            value={String(data.summary.averageAqi)}
            detail={`主污染物：${data.summary.dominantPollutant}`}
          />
          <MetricCard
            label="重点关注城市"
            value={data.summary.maxAqiCity}
            detail={`AQI均值 ${data.summary.maxAqi}`}
            tone="amber"
          />
          <MetricCard
            label="空气最佳城市"
            value={data.summary.bestCity}
            detail={`AQI均值 ${data.summary.bestAqi}`}
          />
          <MetricCard
            label="更新时间"
            value={data.summary.updateTime}
            detail={data.summary.reportSource}
            tone="blue"
          />
        </div>

        <main className="grid min-h-0 flex-1 grid-cols-5 grid-rows-2 gap-3">
          <Panel
            title="全国城市AQI空间分布"
            subtitle="重点城市散点与空气质量等级"
            icon={<MapPinned size={18} />}
            className="col-span-2 row-span-2 chart-enter-delay-1"
          >
            <AirQualityMap data={data.mapPoints} />
          </Panel>

          <Panel
            title="AQI城市排行"
            subtitle="周期均值最高的城市"
            icon={<BarChart3 size={18} />}
            className="chart-enter-delay-2"
          >
            <AqiRank data={data.cityRank} />
          </Panel>

          <Panel
            title="AQI等级分布"
            subtitle="城市日样本结构"
            icon={<ShieldCheck size={18} />}
            className="chart-enter-delay-3"
          >
            <LevelDistribution data={data.levelDistribution} />
          </Panel>

          <Panel
            title="污染物玫瑰图"
            subtitle="CO按100倍展示便于比较"
            icon={<Wind size={18} />}
            className="chart-enter-delay-4"
          >
            <PollutantRose data={data.pollutantMix} />
          </Panel>

          <Panel
            title="全国AQI趋势与预测"
            subtitle={data.summary.forecastNote}
            icon={<Activity size={18} />}
            className="chart-enter-delay-5"
          >
            <AqiTrend data={data.trend} />
          </Panel>

          <Panel
            title="重点城市日期热力图"
            subtitle="排行前列城市逐日AQI变化"
            icon={<RefreshCw size={18} />}
            className="col-span-2 chart-enter-delay-5"
          >
            <CityHeatmap data={data.cityHeatmap} />
          </Panel>
        </main>

        <footer className="dashboard-footer">
          {data.conclusions.map((item) => (
            <span key={item}>{item}</span>
          ))}
        </footer>
      </div>
    </div>
  );
}

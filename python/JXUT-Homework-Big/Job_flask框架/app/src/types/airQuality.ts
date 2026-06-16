export interface SummaryData {
  title: string;
  dateRange: string;
  cityCount: number;
  averageAqi: number;
  maxAqiCity: string;
  maxAqi: number;
  bestCity: string;
  bestAqi: number;
  dominantPollutant: string;
  dataSource: string;
  reportSource: string;
  updateTime: string;
  forecastNote: string;
}

export interface MapPoint {
  name: string;
  value: [number, number, number];
  aqi: number;
  level: string;
  dominant: string;
}

export interface CityRankData {
  cities: string[];
  values: number[];
  bestCities: string[];
  bestValues: number[];
}

export interface TrendData {
  dates: string[];
  observed: Array<number | null>;
  forecast: Array<number | null>;
}

export interface PollutantData {
  name: string;
  value: number;
  rawValue: number;
  unit: string;
}

export interface HeatmapData {
  cities: string[];
  dates: string[];
  values: [number, number, number][];
}

export interface LevelDistributionData {
  name: string;
  value: number;
  color: string;
}

export interface AirQualityDashboardData {
  summary: SummaryData;
  mapPoints: MapPoint[];
  cityRank: CityRankData;
  trend: TrendData;
  pollutantMix: PollutantData[];
  cityHeatmap: HeatmapData;
  levelDistribution: LevelDistributionData[];
  conclusions: string[];
}

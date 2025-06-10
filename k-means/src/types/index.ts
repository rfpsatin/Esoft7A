export interface Point {
  id: string;
  x: number;
  y: number;
  clusterId: number;
  isCentroid: boolean;
  originalValue?: string;
  numericValue?: number;
}

export interface Cluster {
  id: number;
  centroid: Point;
  points: Point[];
}
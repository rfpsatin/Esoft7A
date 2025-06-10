import { Point } from '../types';

export function calculateEuclideanDistance(point1: Point, point2: Point): number {
  const dx = point2.x - point1.x;
  const dy = point2.y - point1.y;
  return Math.sqrt(dx * dx + dy * dy);
}

export function calculateCentroid(points: Point[]): Point {
  if (points.length === 0) {
    throw new Error('Cannot calculate centroid of empty cluster');
  }

  const sum = points.reduce(
    (acc, point) => ({
      x: acc.x + point.x,
      y: acc.y + point.y,
    }),
    { x: 0, y: 0 }
  );

  return {
    id: `centroid-${Date.now()}`,
    x: sum.x / points.length,
    y: sum.y / points.length,
    clusterId: points[0].clusterId,
    isCentroid: true,
  };
}

export function findNearestCluster(point: Point, clusters: Point[]): number {
  let minDistance = Infinity;
  let nearestClusterId = -1;

  clusters.forEach((centroid) => {
    const distance = calculateEuclideanDistance(point, centroid);
    if (distance < minDistance) {
      minDistance = distance;
      nearestClusterId = centroid.clusterId;
    }
  });

  return nearestClusterId;
}

export function categoricalToNumeric(value: string): number {
  return value.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
}
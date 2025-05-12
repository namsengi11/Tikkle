import React from "react";
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

// Interface for line chart data
export interface LineChartData {
  date: string;
  [key: string]: string | number;
}

interface LineChartProps {
  data: LineChartData[];
  lines: {
    dataKey: string;
    color: string;
  }[];
  xAxisDataKey?: string;
  legendPosition?: "right" | "bottom" | "top" | "left";
}

const LineChart: React.FC<LineChartProps> = ({
  data,
  lines,
  xAxisDataKey = "date",
  legendPosition = "bottom",
}) => {
  // Calculate appropriate margins based on legend position
  const getChartMargins = () => {
    const baseMargin = { top: 5, right: 30, left: 20, bottom: 5 };

    switch (legendPosition) {
      case "right":
        return { ...baseMargin, right: 60 };
      case "left":
        return { ...baseMargin, left: 60 };
      case "top":
        return { ...baseMargin, top: 30 };
      case "bottom":
        return { ...baseMargin, bottom: 30 };
      default:
        return baseMargin;
    }
  };

  return (
    <div className="lineChartContainer">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsLineChart data={data} margin={getChartMargins()}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey={xAxisDataKey}
            padding={{ left: 10, right: 10 }}
            tick={{ fontSize: 12, dy: 5 }}
            tickMargin={5}
          />
          <YAxis
            padding={{ top: 10, bottom: 10 }}
            tick={{ fontSize: 12, dx: -5 }}
            tickMargin={5}
          />
          <Tooltip />
          <Legend
            layout="vertical"
            align="right"
            verticalAlign="middle"
            wrapperStyle={{ paddingLeft: 20 }}
          />
          {lines.map((line, index) => (
            <Line
              key={`line-${index}`}
              type="monotone"
              dataKey={line.dataKey}
              stroke={line.color}
            />
          ))}
        </RechartsLineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default LineChart;

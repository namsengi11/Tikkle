import React from "react";
import {
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";

// Add type interface for the label props
interface CustomizedLabelProps {
  cx: number;
  cy: number;
  midAngle: number;
  innerRadius: number;
  outerRadius: number;
  percent: number;
  index: number;
  name: string;
}

// Add interface for PieChartData
export interface PieChartData {
  name: string;
  value: number;
}

interface PieChartProps {
  data: PieChartData[];
  colors: string[];
}

const PieChart: React.FC<PieChartProps> = ({ data, colors }) => {
  // Render custom label function
  const renderCustomizedLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
    index,
    name,
  }: CustomizedLabelProps) => {
    const RADIAN = Math.PI / 180;
    const radius = outerRadius * 1.35;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="#000000"
        textAnchor={x > cx ? "start" : "end"}
        dominantBaseline="central"
      >
        {`${name} ${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="pieChartContainer">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsPieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={true}
            label={renderCustomizedLabel}
            outerRadius={80}
            innerRadius={32}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={colors[index % colors.length]}
              />
            ))}
          </Pie>
        </RechartsPieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PieChart;

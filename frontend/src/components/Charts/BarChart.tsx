import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface BarChartProps {
  data: Array<{
    name: string;
    [key: string]: string | number;
  }>;
  legendPosition?: "right" | "bottom" | "top" | "left";
}

const BarChart: React.FC<BarChartProps> = ({
  data,
  legendPosition = "bottom",
}) => {
  // Configure legend based on position
  const getLegendProps = () => {
    switch (legendPosition) {
      case "right":
        return {
          layout: "vertical",
          align: "right",
          verticalAlign: "middle",
          wrapperStyle: { paddingLeft: 20 },
        };
      case "left":
        return {
          layout: "vertical",
          align: "left",
          verticalAlign: "middle",
          wrapperStyle: { paddingRight: 20 },
        };
      case "top":
        return {
          layout: "horizontal",
          align: "center",
          verticalAlign: "top",
          wrapperStyle: { paddingBottom: 10 },
        };
      case "bottom":
      default:
        return {
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom",
          wrapperStyle: { paddingTop: 10 },
        };
    }
  };

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
    <div className="barChartContainer">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsBarChart data={data} margin={getChartMargins()}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="name"
            padding={{ left: 10, right: 10 }}
            tick={{ fontSize: 12, dy: 3 }}
            tickMargin={3}
          />
          <YAxis
            padding={{ top: 10 }}
            tick={{ fontSize: 12, dx: -3 }}
            tickMargin={3}
            label={{
              value: "위험 지수",
              angle: -90,
              position: "outsideLeft",
            }}
          />
          <Tooltip />
          <Legend {...getLegendProps()} />
          <Bar dataKey="떨어짐" fill="#E57300" />
          <Bar dataKey="넘어짐" fill="#FF8C1A" />
          <Bar dataKey="화재" fill="#FFB61A" />
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BarChart;

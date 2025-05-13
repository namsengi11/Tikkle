import "./Dashboard.css";
import BarChart from "../Charts/BarChart";
import PieChart from "../Charts/PieChart";
import LineChart from "../Charts/LineChart";

const Dashboard = () => {
  // Mock data for pie chart
  const pieChartData = [
    { name: "추락", value: 30 },
    { name: "화상", value: 20 },
    { name: "감전", value: 10 },
    { name: "절단", value: 40 },
  ];

  // Bar chart data reformatted for recharts
  const barChartData = [
    { name: "평택 공장", 떨어짐: 4.2, 넘어짐: 2.4, 화재: 2.1 },
    { name: "청주 공장", 떨어짐: 3.8, 넘어짐: 2.1, 화재: 1.9 },
    { name: "대전 공장", 떨어짐: 3.2, 넘어짐: 1.8, 화재: 1.5 },
  ];

  const lineChartData = [
    { date: "1월", 평택: 4.5, 청주: 7.2, 대전: 3.0 },
    { date: "2월", 평택: 5.0, 청주: 7.0, 대전: 3.5 },
    { date: "3월", 평택: 5.2, 청주: 7.5, 대전: 3.2 },
    { date: "4월", 평택: 5.5, 청주: 7.4, 대전: 3.2 },
  ];

  const lineChartLines = [
    { dataKey: "평택", color: "#E57300" },
    { dataKey: "청주", color: "#FF8C1A" },
    { dataKey: "대전", color: "#FFB61A" },
  ];

  const COLORS = [
    "#E57300",
    "#FF8C1A",
    "#FA9E00",
    "#FFB61A",
    "#FAA700",
    "#FFBE1A",
  ];

  return (
    <div className="container">
      <div className="firstRowContainer">
        <div className="dashboardCell">
          <h2 className="cardTitle">위험도 지수</h2>
          <div className="card">
            <div className="FactoryRiskBox">
              <div className="FactoryRiskScore">
                <p>5.5</p>
              </div>
              <div className="FactoryName">
                <p>평택 공장</p>
              </div>
            </div>
            <div className="FactoryRiskBox">
              <div className="FactoryRiskScore">
                <p>7.4</p>
              </div>
              <div className="FactoryName">
                <p>청주 공장</p>
              </div>
            </div>
            <div className="FactoryRiskBox">
              <div className="FactoryRiskScore">
                <p>3.2</p>
              </div>
              <div className="FactoryName">
                <p>대전 공장</p>
              </div>
            </div>
          </div>
        </div>
        <div className="dashboardCell">
          <h2 className="cardTitle">AI 기반 위험성 평가</h2>
          <div className="card">
            <p className="AIEvaluation">
              <mark className="AIEvaluationText">
                오늘은 어제에 비해 대전 공장에서 화재의 위험이 약 4.6%
                증가했어요. 작업 전에 직원들에게 화재 관련 안전 교육을 할 것을
                추천해요.
              </mark>
            </p>
          </div>
        </div>
      </div>
      <div className="followingRowContainer">
        <div className="dashboardCell">
          <h2 className="cardTitle">공장별 위험 요소</h2>
          <div className="card">
            <BarChart data={barChartData} legendPosition="right" />
          </div>
        </div>
        <div className="dashboardCell">
          <h2 className="cardTitle">위험요소 테이블</h2>
          <div className="card">
            <PieChart data={pieChartData} colors={COLORS} />
          </div>
        </div>
      </div>
      <div className="followingRowContainer">
        <div className="dashboardCell">
          <h2 className="cardTitle">월별 위험 요소 발생 추이</h2>
          <div className="card">
            <div style={{ width: "100%", height: "90%" }}>
              <LineChart
                data={lineChartData}
                lines={lineChartLines}
                legendPosition="right"
              />
            </div>
          </div>
        </div>
        <div className="dashboardCell">
          <h2 className="cardTitle">LLM 분석결과 요약 및 ESG 판단</h2>
          <div className="card">
            <img
              src="/esg_report.png"
              alt="esg_report"
              style={{
                width: "40%",
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

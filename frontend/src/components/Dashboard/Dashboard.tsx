import "./Dashboard.css";

const Dashboard = () => {
  return (
    <div className="container">
      <div className="rowContainerFifth">
        <div className="card">
          <h2 className="cardTitle">위험요소 현황</h2>
        </div>
        <div className="card">
          <h2 className="cardTitle">AI 위험성 평가</h2>
        </div>
      </div>
      <div className="rowContainerTwoFifth">
        <div className="card">
          <h2 className="cardTitle">고위험 작업장 현황</h2>
        </div>
        <div className="card">
          <h2 className="cardTitle">위험요소 테이블</h2>
        </div>
      </div>
      <div className="rowContainerTwoFifth">
        <div className="card">
          <h2 className="cardTitle">일자별 위험지수 그래프</h2>
        </div>
        <div className="card">
          <h2 className="cardTitle">LLM 분석결과 요약 및 ESG 판단</h2>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

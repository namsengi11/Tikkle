import { Factory } from "./Factory";
import { Category } from "./Category";

export class Incident {
  id: number;
  threatType: Category;
  threatLevel: number;
  workType: Category;
  checks: Map<string, boolean>;
  description: string;
  date: Date;
  factory: Factory;
  additionalData: Record<string, any>;

  constructor(
    id: number,
    threatType: Category,
    threatLevel: number,
    workType: Category,
    checks: Map<string, boolean>,
    description: string,
    date: Date,
    factory: Factory,
    additionalData: Record<string, any> = {}
  ) {
    this.id = id;
    this.threatType = threatType;
    this.threatLevel = threatLevel;
    this.workType = workType;
    this.checks = checks;
    this.description = description;
    this.date = date;
    this.factory = factory;
    this.additionalData = additionalData;
  }

  getRelatedInfoInString() {
    const relatedInfo: [string, string][] = [
      ["위험요소 종류", this.threatType.name],
      ["위험요소 레벨", this.threatLevel.toString()],
      ["작업 종류", this.workType.name],
      ["확인 항목", Array.from(this.checks.keys()).join(", ")],
      ["설명", this.description],
      ["발생 공장", this.factory.name],
      ["발생 날짜", this.date.toLocaleDateString()],
    ];
    return relatedInfo;
  }

  static fromJson(json: any) {
    const {
      id = 0,
      threatType = new Category(0, ""),
      threatLevel = 0,
      workType = new Category(0, ""),
      checks = new Map<string, boolean>(),
      description = "",
      date,
      factory,
      ...restProps
    } = json;

    return new Incident(
      id,
      threatType,
      threatLevel,
      workType,
      checks,
      description,
      date ? new Date(date) : new Date(),
      factory,
      restProps
    );
  }
}

import { Factory } from "./Factory";

export class Incident {
  id: number;
  title: string;
  description: string;
  date: Date;
  factory: Factory;
  additionalData: Record<string, any>;

  constructor(
    id: number,
    title: string,
    description: string,
    date: Date,
    factory: Factory,
    additionalData: Record<string, any> = {}
  ) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.date = date;
    this.factory = factory;
    this.additionalData = additionalData;
  }

  getRelatedInfoInString() {
    const relatedInfo: [string, string][] = [
      ["산재 종류", this.title],
      ["발생 공장", this.factory.name],
      ["발생 날짜", this.date.toLocaleDateString()],
    ];
    return relatedInfo;
  }

  static fromJson(json: any) {
    const {
      id = 0,
      title = "",
      description = "",
      date,
      factory,
      ...restProps
    } = json;

    return new Incident(
      id,
      title,
      description,
      date ? new Date(date) : new Date(),
      factory,
      restProps
    );
  }
}

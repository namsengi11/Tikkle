export class Incident {
  id: number;
  title: string;
  description: string;
  date: Date;
  factoryId: number;
  [key: string]: any;

  constructor(
    id: number,
    title: string,
    description: string,
    date: Date,
    factoryId: number,
    ...otherProps: any
  ) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.date = date;
    this.factoryId = factoryId;
  }
}

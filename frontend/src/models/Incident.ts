export class Incident {
  id: number;
  title: string;
  description: string;
  date: Date;
  factory_id: number;

  constructor(
    id: number,
    title: string,
    description: string,
    date: Date,
    factory_id: number
  ) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.date = date;
    this.factory_id = factory_id;
  }
}

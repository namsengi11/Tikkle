export class Category {
  id: number;
  name: string;

  constructor(id: number, name: string) {
    this.id = id;
    this.name = name;
  }

  static createFromRange(object: any) {
    return new Category(object.id ?? 0, object.range ?? "");
  }

  toString() {
    return this.name;
  }
}

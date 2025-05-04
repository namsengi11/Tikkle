export class Factory {
  id: number;
  name: string;

  constructor(id: number, name: string) {
    this.id = id;
    this.name = name;
  }

  toString(): string {
    return this.name;
  }
}

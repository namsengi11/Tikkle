import { Category } from "./Category";

export class Worker {
  id: number;
  name: string;
  ageRange: Category;
  sex: string;
  workExperienceRange: Category;

  constructor(
    id: number,
    name: string,
    ageRange: Category,
    sex: string,
    workExperienceRange: Category
  ) {
    this.id = id;
    this.name = name;
    this.ageRange = ageRange;
    this.sex = sex;
    this.workExperienceRange = workExperienceRange;
  }
}

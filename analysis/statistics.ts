import type { IFStatistics } from "../common/interface";

class Statistics implements IFStatistics {
    mean(group: Array<number>): number {
        group.
    }
    median(group: Array<number>): number {
        throw new Error("Method not implemented.");
    }
    max(group: Array<number>): number {
        throw new Error("Method not implemented.");
    }
    min(group: Array<number>): number {
        throw new Error("Method not implemented.");
    }
    covariance(group_1: Array<number>, group_1_mean: number | null, group_2: Array<number>, group_2_mean: number | null): number {
        throw new Error("Method not implemented.");
    }

}


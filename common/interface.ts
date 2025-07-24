import type { Interface } from "readline";
import type { DeviationSpamAnalysisResult } from "./type";
import type { Queue } from "./queue";

export interface IFTestPromptProcesser {
    collectionSize: number
    readline: Interface


    setMainSection(): void
    displaySection(title: string, description: string ): void
}

export interface IFDeviationBaseSpammmingDetector {
    epsilon: number,
    timestamp: Date,
    timestampQueue: Queue<number>
    timeoutLimit: number // milli-seocnd

    collectTimestamp(timestamp: number): void
    getRepetitionScoreArray(): DeviationSpamAnalysisResult
    getDelayArray(): Array<number>
}

export interface IFQueue<T> { 
    put(data:T): IFQueue<T>
    get(): T | undefined
    display(): void
    asArray(): Array<T>
}
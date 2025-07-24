import readline from "readline";
import type { IFTestPromptProcesser } from "./common/interface";
import type { MessageTimestampElement } from "./common/type";


export class TestPromptProcesser implements IFTestPromptProcesser {
    collectionSize: number = NaN;
    readline!: readline.Interface;

    constructor(collectCount: number = 0) {
        this.readline = readline.createInterface({
          input: process.stdin,
          output: process.stdout,
        });
        this.collectionSize = collectCount
    }

    setMainSection(): void {
        this.readline.question(`[ test spamming section ]`, answer => {
            const collect = new Array<MessageTimestampElement>()

            if (this.collectionSize >= 3) {
                
            } else {
                collect.push({
                    timestamp: new Date().toISOString(),
                    message: answer
                })
            }
        
        });
    }

    getAnalysis(): void {
        throw new Error("Method not implemented.");
    }

    displaySection(title: string, description: string): void {
        this.readline.question(`[ test spamming section ]`, answer => {

        })
    }

}

import { UserDetail } from "./UserProperties";

export interface UserToProjectFull {
    userId?: string;
    projectId?: string;
    role?: string;
    active?: boolean;
    datCreation?: string;
    users?: Array<UserDetail>;
}

export interface ProjectFull {
    projectName?: string;
    descrizioneProgetto?: string;
    datInizio?: string;
    datFine?: string;
    stato?: string;
    avanzamento?: number;
    costo?: number;
    userToProjects?: Array<UserToProjectFull>;
    id: string;
}
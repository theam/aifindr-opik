import { Link } from "@tanstack/react-router";
import copy from "clipboard-copy";
import sortBy from "lodash/sortBy";
import {
  Book,
  Copy,
  GraduationCap,
  Grip,
  KeyRound,
  LogOut,
  Settings,
  Shield,
  UserPlus,
} from "lucide-react";
import { useState } from "react";

import QuickstartDialog from "@/components/pages-shared/onboarding/QuickstartDialog/QuickstartDialog";
import TooltipWrapper from "@/components/shared/TooltipWrapper/TooltipWrapper";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useToast } from "@/components/ui/use-toast";
import { APP_VERSION } from "@/constants/app";
import { buildDocsUrl, cn, maskAPIKey } from "@/lib/utils";
import useAppStore from "@/store/AppStore";
import api from "./api";
import useAllUserWorkspaces from "./useAllUserWorkspaces";
import useUser from "./useUser";
import { buildUrl } from "./utils";

const UserMenu = () => {
  const { toast } = useToast();
  const [openQuickstart, setOpenQuickstart] = useState(false);
  const workspaceName = useAppStore((state) => state.activeWorkspaceName);
  const { data: user } = useUser();
  const { data: workspaces } = useAllUserWorkspaces({
    enabled: !!user?.loggedIn,
  });

  console.log("User and workspaces: ", user, workspaces);

  const workspace = workspaces?.find(
    (workspace) => workspace.workspaceName === workspaceName,
  );

  if (
    !user ||
    !user.loggedIn ||
    !workspaces
  ) {
    return null;
  }

  const handleSwitchToEM = () => {
    window.location.href = buildUrl(
      workspaceName,
      workspaceName,
      "&changeApplication=em",
    );
  };

  const renderAvatar = (clickable = false) => {
    return (
      <Avatar className={cn(clickable ? "cursor-pointer" : "")}>
        <AvatarImage src={user.profileImages.small} />
        <AvatarFallback>{user.userName.charAt(0).toUpperCase()}</AvatarFallback>
      </Avatar>
    );
  };

  const renderAppSelector = () => {
    return (
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="icon">
            <Grip className="size-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuLabel>Your apps</DropdownMenuLabel>

          <DropdownMenuGroup>
            <DropdownMenuItem
              className="flex cursor-pointer flex-row gap-3"
              onClick={handleSwitchToEM}
            >
              <span className="flex size-6 items-center justify-center rounded-[6px] bg-[#6C6FF7] text-[8px] font-medium text-white">
                EM
              </span>
              <span>Experiment management</span>
            </DropdownMenuItem>

            <DropdownMenuItem className="flex cursor-pointer flex-row gap-3">
              <span className="flex size-6 items-center justify-center rounded-[6px] bg-[#52AEA4] text-[8px] font-medium text-white">
                LLM
              </span>

              <span>LLM Evaluation (Opik)</span>
            </DropdownMenuItem>
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    );
  };

  const renderUserMenu = () => {
    return (
      <DropdownMenu>
        <DropdownMenuTrigger asChild>{renderAvatar(true)}</DropdownMenuTrigger>
        <DropdownMenuContent className="w-60" align="end">
          <div className="flex items-center gap-2 px-4 py-2">
            {renderAvatar()}
            <TooltipWrapper content={user.userName}>
              <span className="comet-body-s-accented truncate text-secondary-foreground">
                {user.userName}
              </span>
            </TooltipWrapper>
          </div>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuSub>
              <DropdownMenuSubTrigger className="cursor-pointer">
                <span className="comet-body-s-accented pr-1">Workspace:</span>
                <span className="comet-body-s truncate">{workspaceName}</span>
              </DropdownMenuSubTrigger>
              <DropdownMenuPortal>
                <DropdownMenuSubContent className="w-60">
                  <div className="max-h-[200px] overflow-auto">
                    {sortBy(
                      workspaces,
                      "workspaceName",
                    ).map((workspace) => (
                      <Link
                        key={workspace.workspaceName}
                        to={`/${workspace.workspaceName}`}
                      >
                        <DropdownMenuCheckboxItem
                          checked={workspaceName === workspace.workspaceName}
                        >
                          <TooltipWrapper content={workspace.workspaceName}>
                            <span className="truncate">
                              {workspace.workspaceName}
                            </span>
                          </TooltipWrapper>
                        </DropdownMenuCheckboxItem>
                      </Link>
                    ))}
                  </div>
                  <DropdownMenuSeparator />
                  <a
                    className="flex justify-center"
                    href={buildUrl(
                      "account-settings/workspaces",
                      workspaceName,
                    )}
                  >
                    <Button variant="link">View all workspaces</Button>
                  </a>
                </DropdownMenuSubContent>
              </DropdownMenuPortal>
            </DropdownMenuSub>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <a href={buildUrl("account-settings", workspaceName)}>
              <DropdownMenuItem className="cursor-pointer">
                <Settings className="mr-2 size-4" />
                <span>Account settings</span>
              </DropdownMenuItem>
            </a>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuItem
              onClick={() => setOpenQuickstart(true)}
              className="cursor-pointer"
            >
              <GraduationCap className="mr-2 size-4" />
              <span>Quickstart guide</span>
            </DropdownMenuItem>
            <a href={buildDocsUrl()} target="_blank" rel="noreferrer">
              <DropdownMenuItem className="cursor-pointer">
                <Book className="mr-2 size-4" />
                <span>Docs</span>
              </DropdownMenuItem>
            </a>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuItem
            className="cursor-pointer"
            onClick={async () => {
              await api.get("auth/logout");
              const randomCacheNumber = Math.floor(1e8 * Math.random());
              window.location.href = buildUrl(
                "",
                "",
                `&cache=${randomCacheNumber}`,
              );
            }}
          >
            <LogOut className="mr-2 size-4" />
            <span>Logout</span>
          </DropdownMenuItem>
          {APP_VERSION ? (
            <>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                className="cursor-pointer justify-center text-muted-slate"
                onClick={() => {
                  copy(APP_VERSION);
                  toast({ description: "Successfully copied version" });
                }}
              >
                <span className="comet-body-xs-accented truncate ">
                  VERSION {APP_VERSION}
                </span>
                <Copy className="ml-2 size-3 shrink-0" />
              </DropdownMenuItem>
            </>
          ) : null}
        </DropdownMenuContent>
      </DropdownMenu>
    );
  };

  return (
    <div className="flex shrink-0 items-center gap-4">
      {renderAppSelector()}
      {renderUserMenu()}

      <QuickstartDialog open={openQuickstart} setOpen={setOpenQuickstart} />
    </div>
  );
};

export default UserMenu;

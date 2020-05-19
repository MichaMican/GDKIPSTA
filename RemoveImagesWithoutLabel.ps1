param(
    [Parameter(mandatory=$true)]
    [String]$pathToImages
)
$NoLabelPath = $pathToImages + "\NoLabels"

function Check-Folder() {
    if(!(Test-Path $NoLabelPath)) {
        New-Item -Path $NoLabelPath -ItemType Directory | Out-Null
    }   
}    
    
function Remove-Images {
    $images = gci $pathToImages | ? {$_.Extension -eq '.jpg'}
    $images | ForEach-Object {
        $labelPath = $_.FullName.Substring(0,$_.FullName.LastIndexOf('.')[0]) + ".txt"
        if(Test-Path $labelPath) {
            if((Get-Content $labelPath) -eq $null) {
                Remove-Item $labelPath -Force
            }
        }else {
            Move-Item -Path $_.FullName -Destination $NoLabelPath -Force
        }
    }
}

function main {
    Check-Folder
    Remove-Images
}

main
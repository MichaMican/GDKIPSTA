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
    $counter = 1
    $images | ForEach-Object {
        $labelPath = $_.FullName.Substring(0,$_.FullName.LastIndexOf('.')[0]) + ".txt"
        $complete = $counter / $images.count * 100
        Write-Progress -Activity "Searching for Images without Label" -Status "Running" -PercentComplete $complete
        if(Test-Path $labelPath) {
            if((Get-Content $labelPath) -eq $null) {
                Remove-Item $labelPath -Force
                Write-Host "Removing Label $($labelPath.Split($labelPath.LastIndexOf('\'),$labelPath.Length-1))" -ForegroundColor Yellow
                Move-Item -Path $_.FullName -Destination $NoLabelPath -Force
                Write-Host "Moving Image $($_.Name)" -ForegroundColor Yellow
            }
        }else {
            Move-Item -Path $_.FullName -Destination $NoLabelPath -Force
            Write-Host "Moving Image $($NoLabelPath.Split($NoLabelPath.LastIndexOf('\\'),$NoLabelPath.Length-1))" -ForegroundColor Yellow
        }
        $counter++
    }
}

function main {
    Check-Folder
    Remove-Images
}

main